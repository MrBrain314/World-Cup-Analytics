import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_matches
from utils.style import inject_css, sidebar_setup

st.set_page_config(page_title="Records", page_icon="🏆", layout="wide")
inject_css()
sidebar_setup(Path(__file__).parent.parent)
st.title("🏆 Records & Anomalies")

matches = load_matches()

# ── Matchs les plus prolifiques ───────────────────────────────────────────────
st.subheader("🔥 Matchs les plus prolifiques")
top_goals = (
    matches.sort_values("TotalGoals", ascending=False)
    .head(15)[["Year", "Round", "HomeTeam", "HomeGoals", "AwayGoals", "AwayTeam", "TotalGoals"]]
    .rename(columns={"Year": "Année", "Round": "Phase", "HomeTeam": "Équipe 1",
                     "HomeGoals": "B1", "AwayGoals": "B2", "AwayTeam": "Équipe 2",
                     "TotalGoals": "Total buts"})
)
st.dataframe(top_goals, use_container_width=True, hide_index=True)

st.divider()

# ── Plus grosses victoires ────────────────────────────────────────────────────
st.subheader("💥 Plus grosses victoires (écart de buts)")
matches["Ecart"] = abs(matches["HomeGoals"] - matches["AwayGoals"])
matches["Vainqueur"] = matches.apply(
    lambda r: r["HomeTeam"] if r["HomeGoals"] > r["AwayGoals"]
    else (r["AwayTeam"] if r["AwayGoals"] > r["HomeGoals"] else "Nul"), axis=1
)
matches["Score"] = matches["HomeGoals"].astype(str) + " - " + matches["AwayGoals"].astype(str)

top_ecart = (
    matches[matches["Ecart"] > 0]
    .sort_values("Ecart", ascending=False)
    .head(10)[["Year", "Round", "HomeTeam", "Score", "AwayTeam", "Ecart", "Vainqueur"]]
    .rename(columns={"Year": "Année", "Round": "Phase", "HomeTeam": "Dom.",
                     "AwayTeam": "Ext.", "Ecart": "Écart"})
)
st.dataframe(top_ecart, use_container_width=True, hide_index=True)

st.divider()

col1, col2 = st.columns(2)

# ── Meilleurs buteurs par équipe ──────────────────────────────────────────────
with col1:
    st.subheader("⚽ Top 15 équipes - Buts marqués (total historique)")
    home_gf = matches.groupby("HomeTeam")["HomeGoals"].sum()
    away_gf = matches.groupby("AwayTeam")["AwayGoals"].sum()
    total_gf = (home_gf.add(away_gf, fill_value=0)
                .sort_values(ascending=False)
                .head(15)
                .reset_index())
    total_gf.columns = ["Équipe", "Buts"]

    fig = px.bar(total_gf, x="Buts", y="Équipe", orientation="h",
                 color="Buts", color_continuous_scale="Reds",
                 text="Buts")
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)",
                      yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

# ── Équipes les moins efficaces défensivement ────────────────────────────────
with col2:
    st.subheader("🚨 Top 15 équipes - Buts encaissés (total historique)")
    home_ga = matches.groupby("HomeTeam")["AwayGoals"].sum()
    away_ga = matches.groupby("AwayTeam")["HomeGoals"].sum()
    total_ga = (home_ga.add(away_ga, fill_value=0)
                .sort_values(ascending=False)
                .head(15)
                .reset_index())
    total_ga.columns = ["Équipe", "Buts encaissés"]

    fig2 = px.bar(total_ga, x="Buts encaissés", y="Équipe", orientation="h",
                  color="Buts encaissés", color_continuous_scale="Blues",
                  text="Buts encaissés")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)",
                       yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Underdog stories : victoires d'équipes outsiders ─────────────────────────
st.subheader("😲 Underdog Stories - Grandes surprises en phase finale")

phases_finales = ["Quarter-finals", "Semi-finals", "Final", "Match for third place",
                  "Third place", "Play-off for third place"]
finales = matches[matches["Round"].isin(phases_finales)].copy()

big_upsets = finales[finales["Ecart"] >= 3][["Year", "Round", "HomeTeam", "Score", "AwayTeam", "Ecart"]]
big_upsets = big_upsets.rename(columns={"Year": "Année", "Round": "Phase",
                                         "HomeTeam": "Dom.", "AwayTeam": "Ext.", "Ecart": "Écart"})
if len(big_upsets) > 0:
    st.dataframe(big_upsets, use_container_width=True, hide_index=True)
else:
    st.info("Aucune victoire avec écart ≥ 3 buts en phase finale.")
