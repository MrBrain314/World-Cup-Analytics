import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_matches, load_cups
from utils.style import inject_css, sidebar_setup

st.set_page_config(page_title="Évolution", page_icon="📈", layout="wide")
inject_css()
sidebar_setup(Path(__file__).parent.parent)
st.title("📈 Évolution du Jeu (1930 - 2014)")

matches = load_matches()
cups    = load_cups()

# ── Buts/match par édition ────────────────────────────────────────────────────
st.subheader("Moyenne de buts par match par édition")
avg_per_year = (
    matches.groupby("Year")
    .agg(AvgGoals=("TotalGoals", "mean"), Matchs=("TotalGoals", "count"))
    .reset_index()
)
avg_per_year["AvgGoals"] = avg_per_year["AvgGoals"].round(2)

fig = go.Figure()
fig.add_trace(go.Bar(x=avg_per_year["Year"], y=avg_per_year["AvgGoals"],
                     name="Moy buts/match", marker_color="#9FE870", opacity=0.85))
fig.add_hline(y=avg_per_year["AvgGoals"].mean(), line_dash="dash",
              line_color="#56cfe1", annotation_text="Moyenne globale",
              annotation_position="top right")
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                  xaxis_title="Année", yaxis_title="Buts / match")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Résultats : Victoire domicile vs extérieur vs nul ────────────────────────
st.subheader("Répartition des résultats par édition")

res_year = matches.groupby(["Year", "Result"]).size().reset_index(name="Count")
fig2 = px.bar(
    res_year, x="Year", y="Count", color="Result",
    barmode="stack",
    color_discrete_map={"Home Win": "#56cfe1", "Away Win": "#f4a261", "Draw": "#8a958d"},
    labels={"Year": "Année", "Count": "Matchs", "Result": "Résultat"},
)
fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

# ── Phase de poule vs phases finales ─────────────────────────────────────────
with col1:
    st.subheader("Buts/match : Poules vs Phases finales")
    def phase(r):
        rd = str(r).lower()
        if any(x in rd for x in ["group", "first round", "preliminary"]):
            return "Phase de poule"
        return "Phase finale"

    matches["Phase"] = matches["Round"].apply(phase)
    phase_avg = matches.groupby("Phase")["TotalGoals"].mean().reset_index()
    phase_avg.columns = ["Phase", "Moy buts/match"]
    phase_avg["Moy buts/match"] = phase_avg["Moy buts/match"].round(2)

    fig3 = px.bar(phase_avg, x="Phase", y="Moy buts/match",
                  color="Phase", text="Moy buts/match",
                  color_discrete_sequence=["#56cfe1", "#9FE870"])
    fig3.update_traces(textposition="outside")
    fig3.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

# ── Distribution des scores ───────────────────────────────────────────────────
with col2:
    st.subheader("Distribution des scores totaux")
    fig4 = px.histogram(
        matches, x="TotalGoals", nbins=15,
        labels={"TotalGoals": "Buts dans le match", "count": "Nombre de matchs"},
        color_discrete_sequence=["#e63946"],
    )
    fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Buts/match selon le format du tournoi ─────────────────────────────────────
st.subheader("Plus il y a d'équipes, moins on marque : buts/match par format")

merged = avg_per_year.merge(cups[["Year", "QualifiedTeams"]], on="Year")
fmt = (merged.groupby("QualifiedTeams")
       .agg(AvgGoals=("AvgGoals", "mean"), Editions=("Year", "count"))
       .reset_index())
fmt["AvgGoals"] = fmt["AvgGoals"].round(2)
fmt["Format"] = fmt["QualifiedTeams"].astype(str) + " équipes"

fig5 = px.bar(
    fmt, x="Format", y="AvgGoals",
    text="AvgGoals",
    color="AvgGoals",
    color_continuous_scale=["#1f6f43", "#2ecc71", "#9FE870"],
    labels={"AvgGoals": "Buts / match (moyenne)", "Format": "Format du tournoi"},
    hover_data={"Editions": True},
)
fig5.update_traces(
    texttemplate="%{text}", textposition="outside",
    textfont=dict(size=15, color="#e6eae7"),
)
fig5.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(range=[0, fmt["AvgGoals"].max() + 0.6]),
)
st.plotly_chart(fig5, use_container_width=True)
st.caption(
    "📉 Tendance nette : les tournois à **13-16 équipes** (1930-1978) affichaient en moyenne "
    "plus de 3,5 buts/match, contre ~2,5 depuis le passage à **32 équipes** (1998-2014). "
    "L'élargissement du tournoi a fait baisser la moyenne offensive."
)
