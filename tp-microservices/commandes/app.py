from flask import Flask, jsonify
import requests

# Création de l'application Flask
app = Flask(__name__)

commandes = [
    {"id": 1, "client_id": 1, "produit": "PC", "montant": 1200},
    {"id": 2, "client_id": 2, "produit": "Livre", "montant": 30},
    {"id": 3, "client_id": 1, "produit": "Casque", "montant": 80}
]

# Adresse du microservice clients
CLIENTS_URL = "http://clients:8080"

# Route pour récupérer toutes les commandes (ex : http://localhost:8080/commandes)
@app.route("/commandes", methods=["GET"])
def get_commandes():
    return jsonify(commandes)

# Route pour récupérer une commande par son ID (ex : http://localhost:8080/commandes/1)
@app.route("/commandes/<int:commande_id>", methods=["GET"])
def get_commande(commande_id):

    # 1. Chercher la commande
    for commande in commandes:

        if commande["id"] == commande_id:

            # 2. Récupérer l'identifiant du client
            client_id = commande["client_id"]

            try:
                # 3. Appeler le microservice clients
                response = requests.get(f"{CLIENTS_URL}/clients/{client_id}", timeout=3)

            except requests.exceptions.RequestException:
                return jsonify({"error": "Le microservice clients est indisponible"}), 503

            # 4. Vérifier si le client existe
            if response.status_code == 404:
                return jsonify({"error": "Client associé introuvable"}), 404

            # 5. Vérifier les autres erreurs HTTP
            if response.status_code != 200:
                return jsonify({"error": "Erreur du microservice clients"}), 502

            # 6. Récupérer le JSON du client
            client = response.json()

            # 7. Construire la réponse finale
            return jsonify({
                "id": commande["id"],
                "produit": commande["produit"],
                "montant": commande["montant"],
                "client": client
            })

    # La commande n'existe pas
    return jsonify({"error": "Commande introuvable"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
