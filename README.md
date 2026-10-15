# Projet-Docker-APIRest-Kafka
Projet mené dans le cadre de l'évaluation du module Tools &amp; Language Data Science en dernière année du cycle ingénieur à CY Tech Cergy. Réalisé en trinôme avec NTOOGUE Khephren et HUANG Xin-Ru.


## Utilisation de Docker Desktop

### Démarrage des conteneurs
* **GUI (Interface graphique) :**
  Ouvrez Docker Desktop > onglet **Containers** > cliquez sur **Start / Stop**.
* **CLI (Terminal) :**
  ```bash
  docker compose up -d   # Lancer tous les services
  docker ps              # Lister les conteneurs actifs
  docker compose down    # Arrêter tous les services

# TP 1 : Micro-services et APIRest

## Architecture & Microservices

Le projet est composé de deux microservices Python / Flask :

1. **`clients`** : Service gérant la liste des clients.
   * **Port interne :** `8080`
   * **Port hôte (Machine) :** `8080`
   * **URL d'accès :** `http://localhost:8080/clients`

2. **`commandes`** : Service gérant les commandes et réalisant un appel REST synchrone vers `clients` pour récupérer les informations de l'acheteur.
   * **Port interne :** `8080`
   * **Port hôte (Machine) :** `8081`
   * **URL d'accès :** `http://localhost:8081/commandes`

```bash
cd tp-microservices
docker compose up -d --build
```

On peut ensuite voir les voyants activés pour les applications commande et clients.

'http://localhost:8081/commandes/1' couple bien les 2 applications

# TP 2 & 3 : Kafka et Prédictions
## Structure

```bash
tp-kafka/
├── docker-compose.yml        # Orchestration Kafka et du microservice prediction
├── clients/                  # Microservice Java/Spring Boot Clients
├── commandes/                # Microservice Java/Spring Boot Commandes
├── prediction/               # Microservice Python de prédiction ML
│   ├── app.py                # Consommateur/Producteur Kafka + Inférence
│   ├── Dockerfile            # Containerisation du service Python
│   ├── modele_commande.pkl   # Modèle ML pré-entraîné
│   └── requirements.txt      # Dépendances Python (kafka-python, pandas, joblib, etc.)
└── README.md
```

### Microservices inclus :
1. **Commandes (Java / Spring Boot)** : Publie les événements de création de commande et écoute les retours de prédiction.
2. **Clients (Java / Spring Boot)** : Consomme le topic `commandes-creees` pour maintenir le suivi et l'historique par client.
3. **Prediction (Python / Scikit-Learn)** : Consomme `clients-a-predire`, applique le modèle ML (`modele_commande.pkl`), évalue la probabilité d'achat et publie le résultat sur `predictions`.

---

## Prérequis

- **Docker** & **Docker Compose**
- **Java 17+** & **Maven** (pour exécuter les services Spring Boot en local si besoin)
- **Python 3.10+** (inclus dans l'image Docker du service `prediction`)

---

## Guide de Démarrage Rapide

### 1. Se placer à la racine du projet
```
cd "/home/cytech/Desktop/Projet Docker/tp-kafka"
```
### 2. Démarrer l'infrastructure Docker
```
docker compose up -d --build

docker ps **Pour vérifier que c'est bien démarré**
```
**Test prédiction**

```
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic clients-a-predire
```
```
{"client_id": 25, "age": 32, "anciennete": 3, "nombre_commandes": 8, "montant_total": 1250, "montant_moyen": 156.25, "jours_depuis_derniere_commande": 12}
```
```
docker compose logs -f prediction
```
**Test Résilience à la panne**
```
docker compose stop prediction
```
On injecte des ajouts comme précedemment

docker compose start prediction



