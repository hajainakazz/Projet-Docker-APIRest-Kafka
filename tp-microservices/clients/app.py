from flask import Flask, jsonify

# Création de l'application Flask
app = Flask(__name__)

# Données clients
clients = [
    {"id": 1, "nom": "Alice", "pays": "France"},
    {"id": 2, "nom": "Alex", "pays": "Belgique"},
    {"id": 3, "nom": "Madeleine", "pays": "France"}
]

# Route pour récupérer tous les clients (ex : http://localhost:8080/clients)
@app.route("/clients", methods=["GET"])
def get_clients():
    return jsonify(clients)

# Route pour récupérer un client par son ID (ex : http://localhost:8080/clients/1)
@app.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    for client in clients:
        if client["id"] == client_id:
            return jsonify(client)

    # Si le client n'est pas trouvé, renvoyer une réponse 404
    return jsonify({"error": "Client introuvable"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
