

🌾 Agritech Answers – Prédiction de Rendement Agricole
Projet P12 – OpenClassrooms – Data Scientist
Ce projet propose une solution complète permettant de prédire le rendement agricole d'une parcelle et de recommander la meilleure culture selon les conditions environnementales.
 Il combine Data Science, API, interface web et pipeline CI/CD.

🛠️ Installation

1️⃣ Cloner le projet

git clone https://github.com/Vagaboss/P12.git
cd P12

2️⃣ Créer un environnement virtuel
Avec Poetry :
poetry install
poetry shell

3️⃣ Lancer l’API FastAPI
uvicorn main:app --reload --port 8000

4️⃣ Lancer l’application Streamlit

streamlit run app.py

🧪 Tests

poetry run pytest -v


🚀 Fonctionnalités principales
🔮 1. Prédiction du rendement
L’utilisateur fournit les caractéristiques de sa parcelle + une culture.


L’API renvoie la prédiction de rendement (t/ha).


🌱 2. Recommandation de culture
L’utilisateur décrit seulement les conditions du terrain.


Le système teste toutes les cultures possibles et renvoie un classement du meilleur rendement.



🧠 Modèle Machine Learning
Le modèle retenu est une régression linéaire, offrant les meilleures performances parmi les modèles testés.
📈 Scores :
RMSE : 0.499


R² : 0.913


Variables influençant le plus le rendement :
Pluviométrie


Fertilisation


Irrigation


Température



🧱 Architecture du projet
API FastAPI → prédiction et recommandation


Application Streamlit → interface utilisateur


Docker → conteneurisation de l’API


Tests unitaires Pytest


Pipeline CI/CD GitHub Actions :


exécute les tests


construit l'image Docker


pousse l'image sur Docker Hub


redéploie l’application Streamlit



🖥️ Comment utiliser ?
API
uvicorn main:app --reload --port 8000

Docs : http://localhost:8000/docs

Streamlit

streamlit run app.py

🐳 Déploiement
L’image Docker est automatiquement générée et poussée sur Docker Hub.


L'application Streamlit est automatiquement redéployée à chaque push sur main.



📌 Conclusion
Agritech Answers propose un outil simple, complet et industrialisé permettant :
d’aider les agriculteurs à choisir la culture la plus rentable,


d’estimer le rendement de manière fiable,


d'exposer un modèle ML via une API robuste,


de fournir une application utilisateur intuitive grâce à Streamlit.
