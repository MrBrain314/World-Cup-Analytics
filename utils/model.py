import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Équipes qualifiées pour 2026 (48 équipes, liste officielle FIFA)
TEAMS_2026 = [
    "Brazil", "Argentina", "France", "Germany", "Spain", "England",
    "Portugal", "Netherlands", "Italy", "Belgium", "Croatia", "Uruguay",
    "Colombia", "Mexico", "USA", "Canada", "Japan", "South Korea",
    "Morocco", "Senegal", "Nigeria", "Egypt", "Ivory Coast", "Ghana",
    "Saudi Arabia", "Iran", "Australia", "New Zealand", "Ecuador",
    "Peru", "Chile", "Venezuela", "Panama", "Costa Rica", "Honduras",
    "Qatar", "Turkey", "Poland", "Denmark", "Sweden", "Switzerland",
    "Austria", "Serbia", "Ukraine", "Wales", "Scotland", "Slovakia", "Slovenia"
]

# Pays hôtes 2026 (avantage)
HOSTS_2026 = ["USA", "Canada", "Mexico"]

# Noms alternatifs pour matcher avec le dataset historique
ALIASES = {
    "Germany": ["Germany FR", "Germany"],
    "Serbia": ["Yugoslavia", "Serbia and Montenegro", "Serbia"],
    "Croatia": ["Croatia"],
    "Ivory Coast": ["Ivory Coast"],
    "South Korea": ["Korea Republic", "South Korea"],
    "USA": ["USA"],
}


def _resolve_name(team, all_teams_in_data):
    """Retourne le nom tel qu'utilisé dans le dataset."""
    if team in all_teams_in_data:
        return team
    for canonical, variants in ALIASES.items():
        if team == canonical:
            for v in variants:
                if v in all_teams_in_data:
                    return v
    return team


@st.cache_data
def build_team_features(matches: pd.DataFrame, cups: pd.DataFrame) -> pd.DataFrame:
    """Construit les features historiques par équipe."""
    all_teams = set(matches["HomeTeam"]) | set(matches["AwayTeam"])
    records = []

    for team in all_teams:
        home = matches[matches["HomeTeam"] == team]
        away = matches[matches["AwayTeam"] == team]

        played = len(home) + len(away)
        if played == 0:
            continue

        wins   = (home["HomeGoals"] > home["AwayGoals"]).sum() + \
                 (away["AwayGoals"] > away["HomeGoals"]).sum()
        draws  = (home["HomeGoals"] == home["AwayGoals"]).sum() + \
                 (away["AwayGoals"] == away["HomeGoals"]).sum()
        losses = played - wins - draws

        gf = home["HomeGoals"].sum() + away["AwayGoals"].sum()
        ga = home["AwayGoals"].sum() + away["HomeGoals"].sum()

        titles   = (cups["Winner"]     == team).sum()
        finals   = (cups["Runners-Up"] == team).sum()
        third    = (cups["Third"]      == team).sum()
        editions = cups[
            (cups["Winner"] == team) | (cups["Runners-Up"] == team) |
            (cups["Third"]  == team) | (cups["Fourth"]     == team)
        ].shape[0]

        # Pondération récente : performances sur les 4 dernières éditions
        recent_years = sorted(matches["Year"].unique())[-4:]
        h_rec = matches[(matches["HomeTeam"] == team) & (matches["Year"].isin(recent_years))]
        a_rec = matches[(matches["AwayTeam"] == team) & (matches["Year"].isin(recent_years))]
        p_rec = len(h_rec) + len(a_rec)
        w_rec = (
            (h_rec["HomeGoals"] > h_rec["AwayGoals"]).sum() +
            (a_rec["AwayGoals"] > a_rec["HomeGoals"]).sum()
        )
        win_rate_recent = w_rec / p_rec if p_rec > 0 else 0

        records.append({
            "Team": team,
            "Played": played,
            "WinRate": wins / played,
            "DrawRate": draws / played,
            "AvgGF": gf / played,
            "AvgGA": ga / played,
            "GoalDiff": (gf - ga) / played,
            "Titles": titles,
            "Finals": finals + titles,
            "Podiums": titles + finals + third,
            "Editions": editions,
            "WinRateRecent": win_rate_recent,
        })

    return pd.DataFrame(records).set_index("Team")


@st.cache_data
def train_model(matches: pd.DataFrame, cups: pd.DataFrame):
    """Entraîne un RandomForest sur les données par édition."""
    features_df = build_team_features(matches, cups)

    # Construire X, y : pour chaque édition, le vainqueur = target
    rows = []
    for _, cup in cups.iterrows():
        year   = cup["Year"]
        winner = cup["Winner"]
        # Toutes les équipes présentes à cette édition
        teams_this_year = set(
            matches[matches["Year"] == year]["HomeTeam"].tolist() +
            matches[matches["Year"] == year]["AwayTeam"].tolist()
        )
        for team in teams_this_year:
            if team not in features_df.index:
                continue
            row = features_df.loc[team].copy()
            row["IsWinner"] = 1 if team == winner else 0
            rows.append(row)

    train_df = pd.DataFrame(rows).dropna()
    X = train_df.drop(columns=["IsWinner"])
    y = train_df["IsWinner"]

    clf = RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42, class_weight="balanced")
    clf.fit(X, y)
    return clf, features_df, X.columns.tolist()


def predict_2026(matches: pd.DataFrame, cups: pd.DataFrame) -> pd.DataFrame:
    """Retourne les probabilités de victoire pour les 48 équipes de 2026."""
    clf, features_df, feature_cols = train_model(matches, cups)
    all_teams_in_data = set(features_df.index)

    raw = []
    for team in TEAMS_2026:
        resolved = _resolve_name(team, all_teams_in_data)
        if resolved in features_df.index:
            feat = features_df.loc[[resolved], feature_cols]
            score = clf.predict_proba(feat)[0][1]
        else:
            score = 0.01  # équipe sans historique
        raw.append((team, score))

    # Normalisation : les probabilités de titre se cumulent à 100 %
    total = sum(s for _, s in raw) or 1
    results = [{
        "Équipe": team,
        "Probabilité (%)": round(score / total * 100, 2),
        "Pays hôte": "🏠" if team in HOSTS_2026 else "",
    } for team, score in raw]

    df_res = pd.DataFrame(results).sort_values("Probabilité (%)", ascending=False).reset_index(drop=True)
    df_res.index += 1
    return df_res
