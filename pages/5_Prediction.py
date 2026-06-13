import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_matches, load_cups
from utils.model import predict_2026, build_team_features
from utils.style import team_flag_img, inject_css, sidebar_setup

st.set_page_config(page_title="Prédiction 2026", page_icon="🤖", layout="wide")
inject_css()
sidebar_setup(Path(__file__).parent.parent)
st.title("🤖 Prédiction - Coupe du Monde 2026")

st.info("""
**Méthodologie** : Un modèle Random Forest est entraîné sur les performances historiques
de chaque équipe (1930 - 2014). Les features incluent le taux de victoire global et récent,
les buts marqués/encaissés, le nombre de titres et podiums. Les pays hôtes (USA, Canada,
Mexique) bénéficient d'un contexte favorable noté dans l'analyse.
""")

matches = load_matches()
cups    = load_cups()

with st.spinner("Entraînement du modèle en cours..."):
    results = predict_2026(matches, cups)

st.divider()

# ── Top 10 favoris ────────────────────────────────────────────────────────────
st.subheader("🏆 Top 10 favoris pour 2026")
top10 = results.head(10).copy()

fig = px.bar(
    top10,
    x="Probabilité (%)", y="Équipe",
    orientation="h",
    text="Probabilité (%)",
    color="Probabilité (%)",
    color_continuous_scale=[[0, "#ffd166"], [0.5, "#e63946"], [1, "#003580"]],
    labels={"Probabilité (%)": "Probabilité de victoire (%)"},
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis={"categoryorder": "total ascending"},
    height=420,
)
st.plotly_chart(fig, use_container_width=True)

# ── Podium visuel ─────────────────────────────────────────────────────────────
st.subheader("🥇 Podium prédit")
top3 = results.head(3)


def podium_card(medal, team, prob, bg, text_color="#1d2330"):
    return f"""
    <div style="height:200px; box-sizing:border-box; background:{bg};
        border-radius:16px; padding:18px; display:flex; flex-direction:column;
        align-items:center; justify-content:center; gap:10px;
        box-shadow:0 4px 14px rgba(0,0,0,0.10);">
        <div style="font-size:34px; line-height:1;">{medal}</div>
        <div>{team_flag_img(team, w=46)}</div>
        <div style="font-size:22px; font-weight:800; color:{text_color};
            text-align:center; white-space:nowrap;">{team}</div>
        <div style="font-size:15px; font-weight:700; color:{text_color};
            opacity:.85;">{prob:.1f}%</div>
    </div>
    """


col1, col2, col3 = st.columns(3)
# Ordre podium : 2e à gauche, 1er au centre, 3e à droite
col1.markdown(podium_card("🥈", top3.iloc[1]["Équipe"], top3.iloc[1]["Probabilité (%)"], "#C0C0C0"),
              unsafe_allow_html=True)
col2.markdown(podium_card("🥇", top3.iloc[0]["Équipe"], top3.iloc[0]["Probabilité (%)"], "#FFD700"),
              unsafe_allow_html=True)
col3.markdown(podium_card("🥉", top3.iloc[2]["Équipe"], top3.iloc[2]["Probabilité (%)"], "#CD7F32"),
              unsafe_allow_html=True)

st.divider()

# ── Tableau complet des 48 équipes ────────────────────────────────────────────
st.subheader("📋 Classement complet des 48 équipes")
st.dataframe(results, use_container_width=True)

st.divider()

# ── Importance des features ───────────────────────────────────────────────────
st.subheader("🔍 Facteurs les plus déterminants (importance des variables)")
from utils.model import train_model
import pandas as pd

clf, _, feature_cols = train_model(matches, cups)
importance = pd.DataFrame({
    "Variable": feature_cols,
    "Importance": clf.feature_importances_,
}).sort_values("Importance", ascending=False)

labels_fr = {
    "WinRate": "Taux de victoire global",
    "WinRateRecent": "Taux de victoire récent (4 dernières éditions)",
    "Titles": "Nombre de titres",
    "Podiums": "Nombre de podiums",
    "Finals": "Nombre de finales",
    "GoalDiff": "Différentiel de buts moyen",
    "AvgGF": "Buts marqués en moyenne",
    "AvgGA": "Buts encaissés en moyenne",
    "Editions": "Éditions en phase finale",
    "Played": "Matchs joués",
    "DrawRate": "Taux de nuls",
}
importance["Variable FR"] = importance["Variable"].map(labels_fr).fillna(importance["Variable"])

fig2 = px.bar(
    importance, x="Importance", y="Variable FR",
    orientation="h",
    color="Importance", color_continuous_scale="Blues",
    text=importance["Importance"].apply(lambda x: f"{x:.3f}"),
)
fig2.update_traces(textposition="outside")
fig2.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis={"categoryorder": "total ascending"},
    height=380,
)
st.plotly_chart(fig2, use_container_width=True)

st.caption("Modèle : Random Forest (300 arbres) • Données : FIFA 1930 - 2014 • #DaCoTChallengeData")
