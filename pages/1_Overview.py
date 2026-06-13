import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_matches, load_cups
from utils.style import inject_css, header, kpi_card, section, sidebar_setup, BADGE_COLORS

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
inject_css()
sidebar_setup(Path(__file__).parent.parent)

matches = load_matches()
cups = load_cups()

header("Vue d'ensemble", "Panorama de l'histoire de la Coupe du Monde de la FIFA · 1930 - 2014")

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_matches = len(matches)
total_goals   = int(matches["TotalGoals"].sum())
avg_goals     = round(total_goals / total_matches, 2)
editions      = cups["Year"].nunique()
countries     = len(set(matches["HomeTeam"].unique()) | set(matches["AwayTeam"].unique()))

cols = st.columns(5)
kpis = [
    ("🏆", editions, "Éditions", "1930 - 2014"),
    ("⚽", f"{total_matches}", "Matchs joués", "phase finale"),
    ("🥅", f"{total_goals}", "Buts marqués", "au total"),
    ("📊", avg_goals, "Buts / match", "moyenne historique"),
    ("🌍", countries, "Nations", "ont participé"),
]
for col, (icon, val, lab, sub), color in zip(cols, kpis, BADGE_COLORS):
    col.markdown(kpi_card(icon, val, lab, sub, color), unsafe_allow_html=True)

st.write("")

# ── Carte du monde + Buts par édition ─────────────────────────────────────────
c1, c2 = st.columns([1.1, 1])

with c1:
    section("🌍 Où se gagne la Coupe du Monde ?", "Nombre de titres par pays")
    titles = cups["Winner"].value_counts().reset_index()
    titles.columns = ["Pays", "Titres"]
    iso = {
        "Brazil": "BRA", "Italy": "ITA", "Germany": "DEU", "Germany FR": "DEU",
        "Argentina": "ARG", "Uruguay": "URY", "France": "FRA", "England": "GBR",
        "Spain": "ESP",
    }
    titles["iso"] = titles["Pays"].map(iso)
    fig_map = px.choropleth(
        titles, locations="iso", color="Titres", hover_name="Pays",
        color_continuous_scale=["#ffd166", "#e63946", "#003580"],
        labels={"Titres": "Titres"},
    )
    fig_map.update_geos(showframe=False, showcoastlines=False,
                        projection_type="natural earth", bgcolor="rgba(0,0,0,0)")
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320,
                          coloraxis_colorbar=dict(title=""))
    st.plotly_chart(fig_map, use_container_width=True)

with c2:
    section("📈 Buts marqués par édition", "Évolution de la production offensive")
    goals_year = matches.groupby("Year")["TotalGoals"].sum().reset_index()
    fig = px.area(goals_year, x="Year", y="TotalGoals",
                  labels={"Year": "Année", "TotalGoals": "Buts"})
    fig.update_traces(line_color="#e63946", fillcolor="rgba(230,57,70,0.18)")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0),
                      height=320)
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ── Affluence + Équipes qualifiées ────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    section("👥 Affluence par édition", "Spectateurs totaux (×1000)")
    fig2 = px.bar(cups.dropna(subset=["Attendance"]), x="Year", y="Attendance",
                  color="Attendance", color_continuous_scale="Blues",
                  labels={"Year": "Année", "Attendance": "Spectateurs (×1000)"})
    fig2.update_layout(coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=0, r=0, t=0, b=0), height=300)
    st.plotly_chart(fig2, use_container_width=True)

with c4:
    section("🏟️ Format du tournoi", "Nombre d'équipes qualifiées")
    fig3 = px.line(cups, x="Year", y="QualifiedTeams", markers=True,
                   labels={"Year": "Année", "QualifiedTeams": "Équipes"})
    fig3.update_traces(line_color="#56cfe1", marker_color="#56cfe1")
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=0, r=0, t=0, b=0), height=300)
    st.plotly_chart(fig3, use_container_width=True)

st.write("")

# ── Tableau des éditions ──────────────────────────────────────────────────────
section("📋 Historique complet des éditions")
st.dataframe(
    cups[["Year", "Country", "Winner", "Runners-Up", "Third", "GoalsScored",
          "QualifiedTeams", "MatchesPlayed"]]
    .rename(columns={"Year": "Année", "Country": "Pays hôte", "Winner": "Vainqueur",
                     "Runners-Up": "Finaliste", "Third": "3ème",
                     "GoalsScored": "Buts", "QualifiedTeams": "Équipes",
                     "MatchesPlayed": "Matchs"}),
    use_container_width=True, hide_index=True,
)
