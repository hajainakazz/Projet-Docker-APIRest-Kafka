import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier


# Jeu de données d'exemple
data = [
    [22, 1, 1, 50, 50, 90, 0],
    [25, 2, 2, 120, 60, 60, 0],
    [28, 3, 5, 500, 100, 30, 1],
    [32, 3, 8, 1250, 156.25, 12, 1],
    [35, 5, 10, 1800, 180, 8, 1],
    [42, 8, 15, 3000, 200, 5, 1],
    [50, 10, 20, 4500, 225, 3, 1],
    [23, 1, 1, 30, 30, 120, 0],
    [27, 2, 3, 150, 50, 80, 0],
    [31, 4, 6, 900, 150, 20, 1],
    [38, 6, 12, 2400, 200, 10, 1],
    [45, 9, 18, 3600, 200, 4, 1],
    [21, 1, 1, 20, 20, 150, 0],
    [29, 2, 2, 100, 50, 100, 0],
    [33, 4, 7, 1050, 150, 15, 1],
    [40, 7, 14, 2800, 200, 7, 1],
    [48, 12, 25, 5000, 200, 2, 1],
    [26, 1, 1, 40, 40, 110, 0],
    [30, 3, 4, 400, 100, 45, 0],
    [36, 5, 9, 1350, 150, 18, 1],
    [43, 8, 16, 3200, 200, 6, 1],
    [24, 2, 1, 25, 25, 130, 0],
    [34, 4, 5, 600, 120, 35, 0],
    [39, 6, 11, 2200, 200, 9, 1]
]


columns = [
    "age",
    "anciennete",
    "nombre_commandes",
    "montant_total",
    "montant_moyen",
    "jours_depuis_derniere_commande",
    "commande"
]

df = pd.DataFrame(data, columns=columns)


# Variables explicatives
X = df[
    [
        "age",
        "anciennete",
        "nombre_commandes",
        "montant_total",
        "montant_moyen",
        "jours_depuis_derniere_commande"
    ]
]

# Variable cible
y = df["commande"]


# Création et entraînement du modèle
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# Sauvegarde du modèle
joblib.dump(model, "modele_commande.pkl")

print("Modèle entraîné avec succès !")
print("Modèle sauvegardé dans modele_commande.pkl")
