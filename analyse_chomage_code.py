"""
Analyse du chômage au Maroc (2010-2025)
Source des données : Haut-Commissariat au Plan (HCP), Maroc
Voir sources.md pour les liens complets vers chaque publication.

Ce script :
1. Importe le dataset local (chomage_maroc_dataset.csv)
2. Calcule quelques statistiques descriptives (variation, moyenne par période)
3. Génère un graphique combinant :
   - l'évolution du taux de chômage national, urbain et rural (2010-2025)
   - une mise en évidence des chocs conjoncturels (COVID-19, sécheresse)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ------------------------------------------------------------------
# 1. Import des données
# ------------------------------------------------------------------
df = pd.read_csv("chomage_maroc_dataset.csv")
df = df.sort_values("annee").reset_index(drop=True)

print("Aperçu du dataset :")
print(df[["annee", "taux_chomage_national_pct", "taux_chomage_urbain_pct",
          "taux_chomage_rural_pct"]])

# ------------------------------------------------------------------
# 2. Quelques statistiques clés utilisées dans le rapport
# ------------------------------------------------------------------
taux_2019 = df.loc[df.annee == 2019, "taux_chomage_national_pct"].values[0]
taux_2020 = df.loc[df.annee == 2020, "taux_chomage_national_pct"].values[0]
taux_2025 = df.loc[df.annee == 2025, "taux_chomage_national_pct"].values[0]
taux_2024 = df.loc[df.annee == 2024, "taux_chomage_national_pct"].values[0]

print(f"\nVariation 2019 -> 2020 (choc Covid)   : {taux_2020 - taux_2019:+.1f} pt")
print(f"Variation 2019 -> 2025 (long terme)    : {taux_2025 - taux_2019:+.1f} pt")
print(f"Variation 2024 -> 2025 (dernière année): {taux_2025 - taux_2024:+.1f} pt")

jeunes_2025 = df.loc[df.annee == 2025, "taux_chomage_jeunes_15_24_pct"].values[0]
print(f"Taux de chômage des 15-24 ans en 2025  : {jeunes_2025}%")

# ------------------------------------------------------------------
# 3. Graphique
# ------------------------------------------------------------------
plt.rcParams["font.size"] = 11
fig, ax = plt.subplots(figsize=(11, 6))

# Zones de choc en arrière-plan (dessinées en premier, sous les courbes)
ax.axvspan(2019.5, 2020.5, color="#f2c9c9", alpha=0.5, zorder=0)
ax.axvspan(2022.5, 2023.5, color="#f2e2b3", alpha=0.5, zorder=0)

# Courbe principale : national (bien visible)
ax.plot(df["annee"], df["taux_chomage_national_pct"],
        marker="o", markersize=6, linewidth=3, color="#c1272d",
        label="National", zorder=3)

# Courbes secondaires : urbain / rural (relient uniquement les points connus,
# sans casser la ligne sur les années sans donnée, ex. 2021)
urb = df.dropna(subset=["taux_chomage_urbain_pct"])
rur = df.dropna(subset=["taux_chomage_rural_pct"])

ax.plot(urb["annee"], urb["taux_chomage_urbain_pct"],
        marker="s", markersize=5, linewidth=1.6, linestyle="--",
        color="#1f6f8b", label="Milieu urbain", zorder=2)
ax.plot(rur["annee"], rur["taux_chomage_rural_pct"],
        marker="^", markersize=5, linewidth=1.6, linestyle="--",
        color="#2e8b57", label="Milieu rural", zorder=2)

# Étiquettes de valeur sur la courbe nationale (une sur deux pour ne pas surcharger)
for i, row in df.iterrows():
    if row["annee"] % 2 == 0 or row["annee"] >= 2023:
        ax.annotate(f"{row['taux_chomage_national_pct']:.1f}",
                    xy=(row["annee"], row["taux_chomage_national_pct"]),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8.5, color="#c1272d", fontweight="bold")

# Légendes des zones de choc, placées au-dessus des bandes, sans flèche qui traverse les courbes
ax.text(2020, 19.0, "Choc Covid-19\n(+2,7 pt)", ha="center", va="top",
        fontsize=9, color="#7a1f1f")
ax.text(2023, 19.0, "Sécheresse &\npertes agricoles", ha="center", va="top",
        fontsize=9, color="#7a5a1f")

ax.set_title("Évolution du taux de chômage au Maroc (2010-2025)",
             fontsize=15, fontweight="bold", pad=38)
ax.set_xlabel("Année")
ax.set_ylabel("Taux de chômage (%)")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0))
ax.set_xticks(df["annee"])
ax.tick_params(axis="x", rotation=0)
ax.grid(axis="y", linestyle=":", alpha=0.5)
ax.set_ylim(0, 20.5)
ax.set_xlim(2009.3, 2025.7)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower center", frameon=False, ncol=3, bbox_to_anchor=(0.5, 1.0))

fig.tight_layout()
fig.savefig("evolution_chomage_maroc.png", dpi=220)
print("\nGraphique enregistré : evolution_chomage_maroc.png")
