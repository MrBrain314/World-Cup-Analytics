# Tirage officiel Coupe du Monde 2026 - 12 groupes de 4 équipes
# Format : (Nom affiché, Code ISO drapeau, Rang FIFA, Confédération)
# Le code ISO sert à charger le vrai drapeau via flagcdn.com

GROUPS_2026 = {
    "A": [("Mexique", "mx", 15, "CONCACAF"),
          ("Afrique du Sud", "za", 60, "CAF"),
          ("Corée du Sud", "kr", 21, "AFC"),
          ("Tchéquie", "cz", 43, "UEFA")],

    "B": [("Canada", "ca", 27, "CONCACAF"),
          ("Bosnie-Herzég.", "ba", 74, "UEFA"),
          ("Qatar", "qa", 52, "AFC"),
          ("Suisse", "ch", 17, "UEFA")],

    "C": [("Brésil", "br", 7, "CONMEBOL"),
          ("Maroc", "ma", 11, "CAF"),
          ("Haïti", "ht", 84, "CONCACAF"),
          ("Écosse", "gb-sct", 36, "UEFA")],

    "D": [("États-Unis", "us", 14, "CONCACAF"),
          ("Paraguay", "py", 39, "CONMEBOL"),
          ("Australie", "au", 24, "AFC"),
          ("Turquie", "tr", 26, "UEFA")],

    "E": [("Allemagne", "de", 9, "UEFA"),
          ("Curaçao", "cw", 82, "CONCACAF"),
          ("Côte d'Ivoire", "ci", 40, "CAF"),
          ("Équateur", "ec", 22, "CONMEBOL")],

    "F": [("Pays-Bas", "nl", 6, "UEFA"),
          ("Japon", "jp", 18, "AFC"),
          ("Suède", "se", 44, "UEFA"),
          ("Tunisie", "tn", 41, "CAF")],

    "G": [("Belgique", "be", 8, "UEFA"),
          ("Égypte", "eg", 34, "CAF"),
          ("Iran", "ir", 20, "AFC"),
          ("Nouvelle-Zélande", "nz", 85, "OFC")],

    "H": [("Espagne", "es", 1, "UEFA"),
          ("Cap-Vert", "cv", 68, "CAF"),
          ("Arabie Saoudite", "sa", 58, "AFC"),
          ("Uruguay", "uy", 16, "CONMEBOL")],

    "I": [("France", "fr", 3, "UEFA"),
          ("Sénégal", "sn", 19, "CAF"),
          ("Irak", "iq", 59, "AFC"),
          ("Norvège", "no", 29, "UEFA")],

    "J": [("Argentine", "ar", 2, "CONMEBOL"),
          ("Algérie", "dz", 35, "CAF"),
          ("Autriche", "at", 23, "UEFA"),
          ("Jordanie", "jo", 66, "AFC")],

    "K": [("Portugal", "pt", 5, "UEFA"),
          ("RD Congo", "cd", 56, "CAF"),
          ("Ouzbékistan", "uz", 57, "AFC"),
          ("Colombie", "co", 13, "CONMEBOL")],

    "L": [("Angleterre", "gb-eng", 4, "UEFA"),
          ("Croatie", "hr", 10, "UEFA"),
          ("Ghana", "gh", 72, "CAF"),
          ("Panama", "pa", 30, "CONCACAF")],
}

# Couleurs par confédération (vives, adaptées au fond sombre)
CONF_COLORS = {
    "UEFA": "#56cfe1",
    "CONMEBOL": "#f4a261",
    "CONCACAF": "#2ecc71",
    "CAF": "#ff6b6b",
    "AFC": "#b794f6",
    "OFC": "#9FE870",
}

# Infos générales du tournoi
TOURNAMENT_INFO = {
    "teams": 48,
    "matches": 104,
    "cities": 16,
    "hosts": ["🇺🇸 USA", "🇨🇦 Canada", "🇲🇽 Mexique"],
    "dates": "11 juin - 19 juil. 2026",
}
