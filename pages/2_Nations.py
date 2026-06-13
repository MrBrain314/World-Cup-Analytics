import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_matches, load_cups
from utils.style import inject_css, kpi_card, team_flag_img, sidebar_setup

st.set_page_config(page_title="Nations", page_icon="🌍", layout="wide")
inject_css()
sidebar_setup(Path(__file__).parent.parent)
st.title("🌍 Domination Historique par Nation")

matches = load_matches()
cups    = load_cups()

# ── Palmarès complet ──────────────────────────────────────────────────────────
palmares = pd.DataFrame({
    "Titres":    cups["Winner"].value_counts(),
    "Finaliste": cups["Runners-Up"].value_counts(),
    "3ème":      cups["Third"].value_counts(),
    "4ème":      cups["Fourth"].value_counts(),
}).fillna(0).astype(int)
palmares["Podiums"] = palmares["Titres"] + palmares["Finaliste"] + palmares["3ème"]
palmares = palmares.sort_values("Titres", ascending=False).reset_index().rename(columns={"index": "Pays"})

st.subheader("Palmarès - Top nations")
fig = px.bar(
    palmares.head(12),
    x="Pays", y=["Titres", "Finaliste", "3ème", "4ème"],
    barmode="stack",
    color_discrete_map={"Titres": "#FFD700", "Finaliste": "#C0C0C0", "3ème": "#CD7F32", "4ème": "#6c757d"},
    labels={"value": "Nombre", "variable": "Classement"},
)
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", legend_title="Classement")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Europe vs Amérique du Sud ─────────────────────────────────────────────────
europe  = ["Italy", "Germany FR", "Germany", "France", "England", "Spain", "Netherlands", "Sweden", "Poland", "Portugal", "Yugoslavia", "Czechoslovakia", "Hungary", "Austria", "Belgium", "Croatia", "Turkey", "Denmark"]
amsud   = ["Brazil", "Argentina", "Uruguay", "Chile", "Peru", "Colombia", "Paraguay", "Bolivia"]

def continent(pays):
    if pays in europe: return "Europe"
    if pays in amsud:  return "Amérique du Sud"
    return "Autre"

cups["Continent_Winner"] = cups["Winner"].apply(continent)
cont_titles = cups["Continent_Winner"].value_counts().reset_index()
cont_titles.columns = ["Continent", "Titres"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align:center;'>Titres par continent</h3>",
                unsafe_allow_html=True)
    fig2 = px.pie(
        cont_titles, names="Continent", values="Titres",
        color_discrete_sequence=["#56cfe1", "#f4a261", "#2ecc71"],
        hole=0.45,
    )
    fig2.update_traces(
        textinfo="value+percent",
        texttemplate="%{value} titres<br>%{percent}",
        insidetextorientation="horizontal",
        textfont=dict(size=15, color="#ffffff"),
        marker=dict(line=dict(color="#ffffff", width=2)),
    )
    fig2.update_layout(
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center", title=""),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("La course aux titres : Europe vs Amérique du Sud")
    cups_sorted = cups.sort_values("Year").copy()
    cups_sorted["Continent_label"] = cups_sorted["Winner"].apply(continent)
    cups_sorted["Titres Europe"] = (cups_sorted["Continent_label"] == "Europe").cumsum()
    cups_sorted["Titres Amérique du Sud"] = (cups_sorted["Continent_label"] == "Amérique du Sud").cumsum()

    race = cups_sorted.melt(
        id_vars="Year",
        value_vars=["Titres Europe", "Titres Amérique du Sud"],
        var_name="Continent", value_name="Titres cumulés",
    )
    race["Continent"] = race["Continent"].str.replace("Titres ", "")

    fig3 = px.line(
        race, x="Year", y="Titres cumulés", color="Continent",
        markers=True,
        color_discrete_map={"Europe": "#56cfe1", "Amérique du Sud": "#f4a261"},
        labels={"Year": "Année"},
    )
    fig3.update_traces(line_width=3, marker_size=7)
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", y=1.12, title=""))
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Performances par équipe ───────────────────────────────────────────────────
st.subheader("Analyse détaillée par équipe")

all_teams = sorted(set(matches["HomeTeam"].unique()) | set(matches["AwayTeam"].unique()))
selected  = st.selectbox("Choisir une équipe", all_teams, index=all_teams.index("Brazil"))

home = matches[matches["HomeTeam"] == selected].copy()
away = matches[matches["AwayTeam"] == selected].copy()

home["W"] = home["HomeGoals"] > home["AwayGoals"]
home["D"] = home["HomeGoals"] == home["AwayGoals"]
home["L"] = home["HomeGoals"] < home["AwayGoals"]
home["GF"] = home["HomeGoals"]
home["GA"] = home["AwayGoals"]

away["W"] = away["AwayGoals"] > away["HomeGoals"]
away["D"] = away["AwayGoals"] == away["HomeGoals"]
away["L"] = away["AwayGoals"] < away["HomeGoals"]
away["GF"] = away["AwayGoals"]
away["GA"] = away["HomeGoals"]

total_p = len(home) + len(away)
total_w = int(home["W"].sum() + away["W"].sum())
total_d = int(home["D"].sum() + away["D"].sum())
total_l = int(home["L"].sum() + away["L"].sum())
total_gf = int(home["GF"].sum() + away["GF"].sum())
total_ga = int(home["GA"].sum() + away["GA"].sum())

win_rate = round(total_w / total_p * 100, 1) if total_p else 0
cols = st.columns(6)
stats = [
    ("⚽", total_p, "Matchs", "joués au total", "#4361ee"),
    ("✅", total_w, "Victoires", f"{win_rate}% de réussite", "#2a9d8f"),
    ("🤝", total_d, "Nuls", "matchs nuls", "#f4a261"),
    ("❌", total_l, "Défaites", "matchs perdus", "#e63946"),
    ("🥅", total_gf, "Buts marqués", "sur l'histoire", "#56cfe1"),
    ("🛡️", total_ga, "Buts encaissés", "sur l'histoire", "#7209b7"),
]
for col, (icon, val, lab, sub, color) in zip(cols, stats):
    col.markdown(kpi_card(icon, val, lab, sub, color), unsafe_allow_html=True)

# Buts par édition
gf_year = home.groupby("Year")["GF"].sum() + away.groupby("Year")["GF"].sum()
gf_year = gf_year.fillna(0).reset_index()
gf_year.columns = ["Year", "Buts marqués"]

fig4 = px.line(gf_year, x="Year", y="Buts marqués", markers=True,
               title=f"Buts marqués par édition - {selected}",
               labels={"Year": "Année"})
fig4.update_traces(line_color="#e63946", marker_color="#e63946")
fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig4, use_container_width=True)
