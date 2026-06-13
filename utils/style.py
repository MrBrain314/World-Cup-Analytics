import streamlit as st
import base64
import plotly.io as pio
import plotly.graph_objects as go

# Palette World Cup 2026 - thème sombre
DARK     = "#0e1512"   # fond
CARD     = "#18211b"   # cartes
CARD_BRD = "rgba(255,255,255,0.07)"
LIME     = "#9FE870"   # accent principal
GREEN    = "#2ecc71"
TEXT     = "#e6eae7"   # texte clair
MUTED    = "#8a958d"   # texte secondaire
GOLD     = "#FFD700"

# Couleurs des badges KPI (icône ronde)
BADGE_COLORS = ["#9FE870", "#2ecc71", "#4ade80", "#f4a261", "#56cfe1"]


def _setup_plotly():
    """Template Plotly sombre appliqué globalement à tous les graphiques."""
    tmpl = go.layout.Template()
    tmpl.layout.paper_bgcolor = "rgba(0,0,0,0)"
    tmpl.layout.plot_bgcolor = "rgba(0,0,0,0)"
    tmpl.layout.font = dict(color="#cfd6d0", family="sans serif")
    tmpl.layout.xaxis = dict(gridcolor="rgba(255,255,255,0.07)",
                             zerolinecolor="rgba(255,255,255,0.12)", linecolor="rgba(255,255,255,0.15)")
    tmpl.layout.yaxis = dict(gridcolor="rgba(255,255,255,0.07)",
                             zerolinecolor="rgba(255,255,255,0.12)", linecolor="rgba(255,255,255,0.15)")
    tmpl.layout.colorway = ["#9FE870", "#2ecc71", "#4ade80", "#56cfe1", "#f4a261", "#a78bfa"]
    pio.templates["wc_dark"] = tmpl
    pio.templates.default = "plotly_dark+wc_dark"


def inject_css():
    """Injecte le CSS global (thème sombre) + le template Plotly."""
    _setup_plotly()
    st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Cartes génériques */
    .wc-card {
        background:#18211b; border-radius:16px; padding:18px 20px;
        box-shadow:0 4px 18px rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.07);
        margin-bottom:12px;
    }

    /* KPI card */
    .kpi {
        background:#18211b; border-radius:16px; padding:16px 12px;
        box-shadow:0 4px 18px rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.07);
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        text-align:center; gap:6px; min-height:150px;
    }
    .kpi .badge {
        width:44px; height:44px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:20px; color:#0e1512; flex-shrink:0; font-weight:800;
    }
    .kpi .kpi-label { font-size:11px; color:#8a958d; font-weight:700;
        text-transform:uppercase; letter-spacing:.3px; margin:0; white-space:nowrap; }
    .kpi .kpi-value { font-size:30px; font-weight:800; color:#f1f5f2;
        line-height:1; margin:0; white-space:nowrap; }
    .kpi .kpi-sub { font-size:11px; color:#6f7a72; margin:0; white-space:nowrap; }

    /* Titre de section */
    .section-title { font-size:20px; font-weight:800; color:#f1f5f2; margin:8px 0 4px 0; }
    .section-sub { font-size:13px; color:#8a958d; margin-bottom:10px; }

    /* En-tête bannière */
    .wc-header {
        background:linear-gradient(120deg,#123524 0%,#0e1512 55%,#1f6f43 150%);
        border:1px solid rgba(159,232,112,0.25);
        border-radius:28px; padding:30px 36px; color:#fff; margin-bottom:18px;
    }
    .wc-header h1 { color:#fff; font-size:30px; font-weight:800; margin:0; }
    .wc-header p { color:#cfe9d8; font-size:14px; margin:6px 0 0 0; }

    /* Sidebar branding */
    .sidebar-brand { text-align:center; padding:6px 0 14px 0; }
    .sidebar-brand .t1 { font-size:11px; color:#9FE870; font-weight:700;
        text-transform:uppercase; letter-spacing:1px; }
    .sidebar-brand .t2 { font-size:18px; font-weight:800; color:#f1f5f2;
        line-height:1.15; margin:2px 0; }
    .sidebar-brand .t3 { font-size:12px; color:#8a958d; }

    /* Pousse le crédit vers le bas de la sidebar */
    [data-testid="stSidebarUserContent"] {
        display:flex; flex-direction:column; min-height:calc(100vh - 230px);
    }
    .sidebar-logo { text-align:center; padding:4px 6px 10px 6px; }
    .sidebar-logo img { width:100%; max-width:180px; border-radius:14px; }

    .sidebar-credit { margin-top:auto; text-align:center; padding-top:20px; }
    .sidebar-credit .sep { height:1px; background:rgba(255,255,255,0.12); margin:0 auto 14px auto; width:70%; }
    .sidebar-credit .tag  { font-size:11px; color:#9FE870; font-weight:700; margin-top:6px; }

    /* Carte de groupe */
    .grp-card { background:#18211b; border-radius:12px; border:1px solid rgba(255,255,255,0.07);
        box-shadow:0 3px 12px rgba(0,0,0,0.35); overflow:hidden; margin-bottom:14px; }
    .grp-head { background:linear-gradient(90deg,#1f6f43,#2ecc71); color:#0e1512;
        font-weight:800; font-size:14px; text-align:center; padding:7px 0; letter-spacing:.5px; }
    .grp-row { display:flex; align-items:center; gap:9px; padding:0 14px;
        height:46px; border-bottom:1px solid rgba(255,255,255,0.06); font-size:13px; }
    .grp-row:last-child { border-bottom:none; }
    .grp-flag { width:26px; flex-shrink:0; display:flex; align-items:center; }
    .grp-flag img { border-radius:3px; box-shadow:0 0 1px rgba(0,0,0,0.6); }
    .grp-name { flex:1; min-width:0; color:#e6eae7; font-weight:600;
        white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .grp-rank { width:46px; text-align:center; color:#f1f5f2; font-weight:800;
        white-space:nowrap; flex-shrink:0; }
    .grp-conf { width:74px; text-align:right; font-size:11px; font-weight:700;
        flex-shrink:0; }
    </style>
    """, unsafe_allow_html=True)


def header(title, subtitle):
    st.markdown(f"""
    <div class="wc-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(icon, value, label, sub="", color="#4361ee"):
    """Retourne le HTML d'une carte KPI (à mettre dans une colonne)."""
    return f"""
    <div class="kpi">
        <div class="badge" style="background:{color};">{icon}</div>
        <p class="kpi-value">{value}</p>
        <p class="kpi-label">{label}</p>
        <p class="kpi-sub">{sub}</p>
    </div>
    """


def section(title, sub=""):
    html = f'<div class="section-title">{title}</div>'
    if sub:
        html += f'<div class="section-sub">{sub}</div>'
    st.markdown(html, unsafe_allow_html=True)


def sidebar_setup(root=None, name=None, role=None):
    """Logo artwork en haut de la sidebar + hashtag en bas. À appeler sur chaque page."""
    from pathlib import Path
    inject_css()
    if root is not None:
        logo = Path(root) / "assets" / "logo.jpg"
        if logo.exists():
            b64 = base64.b64encode(logo.read_bytes()).decode()
            st.sidebar.markdown(f"""
            <div class="sidebar-logo">
                <img src="data:image/jpeg;base64,{b64}">
            </div>
            """, unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div class="sidebar-credit">
        <div class="sep"></div>
        <div class="tag">#DaCoTChallengeData</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_brand():
    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <div class="t1">FIFA World Cup 26™</div>
        <div class="t2">⚽ Coupe du Monde<br>2026</div>
        <div class="t3">48 équipes · 16 villes · 104 matchs</div>
        <div class="t3">🇺🇸 🇨🇦 🇲🇽</div>
    </div>
    """, unsafe_allow_html=True)


def flag_img(iso, w=26):
    """Renvoie le HTML d'un vrai drapeau (flagcdn.com) à partir d'un code ISO.
    Le format /w40/ est toujours disponible quelle que soit la largeur affichée."""
    return (f'<img src="https://flagcdn.com/w40/{iso}.png" '
            f'width="{w}" style="border-radius:3px; box-shadow:0 0 1px rgba(0,0,0,0.4);" '
            f'alt="{iso}">')


def group_card(letter, teams, conf_colors):
    """Génère le HTML d'une carte de groupe. teams = [(nom, iso, rang, conf), ...]"""
    rows = ""
    for name, iso, rank, conf in teams:
        color = conf_colors.get(conf, "#8b93a7")
        rows += f"""<div class="grp-row">
            <span class="grp-flag">{flag_img(iso)}</span>
            <span class="grp-name">{name}</span>
            <span class="grp-rank">{rank}</span>
            <span class="grp-conf" style="color:{color};">{conf}</span>
        </div>"""
    return f"""<div class="grp-card">
        <div class="grp-head">GROUPE {letter}</div>
        {rows}
    </div>"""


def sidebar_author(name="OURO-TAGBA Bastou", role="Data Analyst"):
    st.sidebar.markdown(f"""
    <div class="author">
        ───────────<br>
        <b>{name}</b><br>{role}<br>
        <span style="font-size:11px;">#DaCoTChallengeData</span>
    </div>
    """, unsafe_allow_html=True)


# ── Drapeaux (emoji) par nom d'équipe du dataset ──────────────────────────────
FLAGS = {
    "Brazil": "🇧🇷", "Argentina": "🇦🇷", "Germany": "🇩🇪", "Germany FR": "🇩🇪",
    "Italy": "🇮🇹", "France": "🇫🇷", "Spain": "🇪🇸", "England": "🏴",
    "Netherlands": "🇳🇱", "Uruguay": "🇺🇾", "Portugal": "🇵🇹", "Belgium": "🇧🇪",
    "Croatia": "🇭🇷", "Sweden": "🇸🇪", "Mexico": "🇲🇽", "USA": "🇺🇸",
    "Chile": "🇨🇱", "Colombia": "🇨🇴", "Poland": "🇵🇱", "Hungary": "🇭🇺",
    "Czechoslovakia": "🇨🇿", "Austria": "🇦🇹", "Yugoslavia": "🇷🇸", "Russia": "🇷🇺",
    "Soviet Union": "🇷🇺", "Switzerland": "🇨🇭", "Denmark": "🇩🇰", "Japan": "🇯🇵",
    "Korea Republic": "🇰🇷", "South Korea": "🇰🇷", "Morocco": "🇲🇦", "Senegal": "🇸🇳",
    "Nigeria": "🇳🇬", "Ghana": "🇬🇭", "Cameroon": "🇨🇲", "Costa Rica": "🇨🇷",
    "Turkey": "🇹🇷", "Ukraine": "🇺🇦", "Peru": "🇵🇪", "Paraguay": "🇵🇾",
    "Ecuador": "🇪🇨", "Saudi Arabia": "🇸🇦", "Iran": "🇮🇷", "Australia": "🇦🇺",
    "Egypt": "🇪🇬", "Ivory Coast": "🇨🇮", "Serbia": "🇷🇸", "Scotland": "🏴",
    "Wales": "🏴", "Canada": "🇨🇦", "Qatar": "🇶🇦", "New Zealand": "🇳🇿",
    "Venezuela": "🇻🇪", "Panama": "🇵🇦", "Honduras": "🇭🇳", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Bolivia": "🇧🇴",
}


def flag(team):
    return FLAGS.get(team, "🏳️")


# Codes ISO par nom d'équipe (anglais, sortie du modèle ML)
ISO_BY_TEAM = {
    "Brazil": "br", "Argentina": "ar", "Germany": "de", "Germany FR": "de",
    "Italy": "it", "France": "fr", "Spain": "es", "England": "gb-eng",
    "Netherlands": "nl", "Uruguay": "uy", "Portugal": "pt", "Belgium": "be",
    "Croatia": "hr", "Sweden": "se", "Mexico": "mx", "USA": "us",
    "Colombia": "co", "Morocco": "ma", "Japan": "jp", "South Korea": "kr",
    "Korea Republic": "kr", "Senegal": "sn", "Nigeria": "ng", "Ghana": "gh",
    "Switzerland": "ch", "Denmark": "dk", "Poland": "pl", "Austria": "at",
    "Serbia": "rs", "Yugoslavia": "rs", "Canada": "ca", "Qatar": "qa",
    "Australia": "au", "Ecuador": "ec", "Peru": "pe", "Chile": "cl",
    "Egypt": "eg", "Ivory Coast": "ci", "Iran": "ir", "Saudi Arabia": "sa",
    "Turkey": "tr", "Ukraine": "ua", "Wales": "gb-wls", "Scotland": "gb-sct",
    "Slovakia": "sk", "Slovenia": "si", "Venezuela": "ve", "Panama": "pa",
    "Costa Rica": "cr", "Honduras": "hn", "New Zealand": "nz", "Paraguay": "py",
}


def team_flag_img(team, w=22):
    iso = ISO_BY_TEAM.get(team)
    return flag_img(iso, w) if iso else ""
