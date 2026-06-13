import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))
from utils.data_loader import load_matches, load_cups
from utils.model import predict_2026
from utils.style import (inject_css, kpi_card, section, sidebar_setup,
                         group_card, flag_img, team_flag_img, BADGE_COLORS)
from data.groups_2026 import GROUPS_2026, CONF_COLORS, TOURNAMENT_INFO

st.set_page_config(page_title="Coupe du Monde 2026", page_icon="🏆", layout="wide")
inject_css()
sidebar_setup(ROOT)

# ── Bannière d'annonce avec logo ──────────────────────────────────────────────
logo = ROOT / "assets" / "logo.jpg"
c_logo, c_txt = st.columns([1, 2.4], vertical_alignment="center")
with c_logo:
    if logo.exists():
        st.image(str(logo), use_container_width=True)
with c_txt:
    st.markdown(f"""
    <div class="wc-header" style="margin:0;">
        <h1>🏆 Coupe du Monde 2026</h1>
        <p>Le rendez-vous mondial revient · {TOURNAMENT_INFO['dates']}<br>
        Premier Mondial à 48 équipes, organisé par les États-Unis, le Canada et le Mexique.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ── KPIs du tournoi ───────────────────────────────────────────────────────────
cols = st.columns(4)
kpis = [
    ("👥", TOURNAMENT_INFO["teams"], "Équipes qualifiées", "format élargi +16 vs 2022"),
    ("⚽", TOURNAMENT_INFO["matches"], "Matchs", TOURNAMENT_INFO["dates"]),
    ("🏟️", TOURNAMENT_INFO["cities"], "Villes hôtes", "USA 11 · CAN 2 · MEX 3"),
    ("🌍", 3, "Pays organisateurs", "USA · Canada · Mexique"),
]
for col, (icon, val, lab, sub), color in zip(cols, kpis, BADGE_COLORS):
    col.markdown(kpi_card(icon, val, lab, sub, color), unsafe_allow_html=True)

st.write("")

# ── Confédérations + Favoris ──────────────────────────────────────────────────
matches = load_matches()
cups = load_cups()

conf_count = {}
for teams in GROUPS_2026.values():
    for _, _, _, conf in teams:
        conf_count[conf] = conf_count.get(conf, 0) + 1
conf_df = pd.DataFrame(list(conf_count.items()), columns=["Confédération", "Équipes"])

PANEL_H = 560  # hauteur commune des deux panneaux
c1, c2 = st.columns(2, gap="large")

with c1:
    with st.container(border=True, height=PANEL_H):
        section("🌐 Équipes par confédération", "Répartition des 48 nations qualifiées")
        fig = px.pie(conf_df, names="Confédération", values="Équipes", hole=0.55,
                     color="Confédération", color_discrete_map=CONF_COLORS)
        fig.update_traces(textinfo="label+value", textfont_size=12)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                          legend=dict(orientation="h", y=-0.08))
        st.plotly_chart(fig, use_container_width=True)

with c2:
    with st.container(border=True, height=PANEL_H):
        section("🏆 Équipes favorites", "Probabilité de titre selon notre modèle ML")
        results = predict_2026(matches, cups)
        top = results.head(5).reset_index(drop=True)
        fav_name = top.iloc[0]["Équipe"]
        fav_prob = top.iloc[0]["Probabilité (%)"]

        axis_max = max(20, round(fav_prob * 1.4))
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fav_prob,
            number={"suffix": " %", "font": {"size": 38, "color": "#f1f5f2"}},
            title={"text": f"<b>{fav_name}</b>", "font": {"size": 22, "color": "#f1f5f2"}},
            gauge={
                "axis": {"range": [0, axis_max], "tickwidth": 1, "tickcolor": "#6f7a72"},
                "bar": {"color": "#9FE870", "thickness": 0.32},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, axis_max * 0.5], "color": "rgba(255,255,255,0.05)"},
                    {"range": [axis_max * 0.5, axis_max], "color": "rgba(255,255,255,0.10)"},
                ],
                "threshold": {"line": {"color": "#2ecc71", "width": 4},
                              "thickness": 0.8, "value": fav_prob},
            },
        ))
        gauge.update_layout(height=240, margin=dict(l=24, r=24, t=52, b=0),
                            paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(gauge, use_container_width=True)

        chasers = top.iloc[1:5].copy()
        rows_html = ""
        for _, r in chasers.iterrows():
            rows_html += f"""<div class="grp-row">
                <span class="grp-flag">{team_flag_img(r['Équipe'])}</span>
                <span class="grp-name">{r['Équipe']}</span>
                <span class="grp-rank" style="color:#e63946;">{r['Probabilité (%)']:.1f}%</span>
            </div>"""
        st.markdown(f'<div class="grp-card">{rows_html}</div>', unsafe_allow_html=True)

st.write("")

# ── Grille des 12 groupes (3 colonnes pour la lisibilité) ─────────────────────
section("🗂️ Les 12 groupes de la phase finale", "Tirage officiel · rang FIFA et confédération")

letters = list(GROUPS_2026.keys())
for i in range(0, 12, 3):
    cols = st.columns(3)
    for col, letter in zip(cols, letters[i:i + 3]):
        col.markdown(group_card(letter, GROUPS_2026[letter], CONF_COLORS),
                     unsafe_allow_html=True)

st.write("")
st.info(
    "ℹ️ **Note méthodologique** : le classement des favoris est établi uniquement à partir "
    "des données historiques de la Coupe du Monde **de 1930 à 2014**. Il reflète donc la "
    "domination passée des nations, et non leur forme actuelle ni les joueurs de 2026. "
    "Certaines équipes en tête (ex. l'Italie) ne sont d'ailleurs pas qualifiées pour cette "
    "édition. À prendre comme une lecture statistique de l'histoire, pas comme un pronostic définitif."
)
