# Image Python légère et stable pour la data
FROM python:3.10-slim

# Ne pas générer de fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Afficher les logs en direct
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier uniquement les dépendances en premier (optimise le build)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet (main.py, models/, data éventuelle, etc.)
COPY . .

# Exposer le port FastAPI
EXPOSE 8000

# Commande de lancement de l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
