import json
import os

import joblib
import pandas as pd

from kafka import KafkaConsumer, KafkaProducer


# Chargement du modèle entraîné
model = joblib.load("modele_commande.pkl")


# Connexion à Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

consumer = KafkaConsumer(
    "clients-a-predire",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id="prediction-group",
    auto_offset_reset="earliest",
    api_version=(3, 0, 0),
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    api_version=(3, 0, 0),
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)


print("Microservice Prediction démarré...")
print("En attente de messages Kafka...")


for message in consumer:

    data = message.value

    print()
    print("================================")
    print("Nouvelle demande de prédiction")
    print("Client :", data["client_id"])

    # Préparation des données pour le modèle
    X = pd.DataFrame([{
        "age": data["age"],
        "anciennete": data["anciennete"],
        "nombre_commandes": data["nombre_commandes"],
        "montant_total": data["montant_total"],
        "montant_moyen": data["montant_moyen"],
        "jours_depuis_derniere_commande":
            data["jours_depuis_derniere_commande"]
    }])

    # Prédiction
    prediction = model.predict(X)[0]
    probabilite = model.predict_proba(X)[0][1]

    print("Prediction :", prediction)
    print("Probabilite :", probabilite)

    # Résultat à envoyer dans Kafka
    resultat = {
        "client_id": data["client_id"],
        "prediction": int(prediction),
        "probabilite_commande": float(probabilite)
    }

    # Envoi vers le topic predictions
    producer.send(
        "predictions",
        value=resultat
    )

    producer.flush()

    print("Résultat envoyé vers Kafka")
    print("================================")
