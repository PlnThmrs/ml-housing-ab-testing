[![CI Pipeline](https://github.com/PlnThmrs/ml-housing-ab-testing/actions/workflows/ci.yml/badge.svg)](https://github.com/PlnThmrs/ml-housing-ab-testing/actions/workflows/ci.yml)

# ML Housing Project

Projet MLOps de prediction de prix immobiliers base sur le dataset California Housing.

L'application est composée de quatre briques :

- un pipeline d'entraînement local
- une couche de prédiction réutilisable
- une API FastAPI
- une interface utilisateur Streamlit

Le workflow principal est simple :

1. entraîner un modèle en local
2. publier le modèle dans MinIO
3. démarrer le backend
4. laisser le backend télécharger le modele depuis MinIO
5. faire des prédictions depuis l'API ou depuis Streamlit

## Objectifs

- séparer le code d'entraînement du code d'inférence
- stocker les modèles dans un stockage objet simple
- proposer un démarrage local reproductible avec Docker Compose
- valider la qualité du projet par tests, lint, formatage et scan securité

## Architecture

```text
ml-housing-project/
|-- backend/
|   |-- app.py
|   `-- storage/s3_client.py
|-- frontend/
|   `-- streamlit_app.py
|-- src/
|   |-- common/
|   |   `-- features.py
|   |-- prediction/
|   |   |-- config.py
|   |   |-- model_loader.py
|   |   |-- predict.py
|   |   `-- schemas.py
|   `-- training/
|       |-- data.py
|       |-- evaluate.py
|       |-- pipeline.py
|       |-- preprocessing.py
|       `-- train.py
|-- scripts/
|   `-- upload_model_to_minio.py
|-- tests/
|-- artifacts/
|   |-- models/
|   `-- metrics/
|-- Docs/
|   `-- user_manual.md
|-- docker-compose.yml
|-- main.py
`-- README.md
```

## Prérequis

### En local sans Docker

- Python 3.10
- pip
- environnement virtuel recommande

### Avec Docker

- Docker Desktop ou Docker Engine
- Docker Compose

## Variables d'environnement

Le projet fournit un modèle d'environnement versionnable :

```powershell
Copy-Item .env.example .env
```

Variables importantes :

- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `MINIO_BUCKET_MODELS`
- `MODEL_OBJECT_NAME`
- `LOCAL_MODEL_PATH`
- `BACKEND_URL`

## Installation locale

### Windows PowerShell

```powershell
python -m venv mon_env
.\mon_env\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev]"
Copy-Item .env.example .env
```

### Linux ou macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev]"
cp .env.example .env
```

## Entraîner un modèle

```powershell
python main.py
```

Effets attendus :

- création d'un modèle versionné dans `artifacts/models`
- mise à jour de `model_latest.joblib`
- création d'un fichier de métriques dans `artifacts/metrics`

## Publier le modèle dans MinIO

```powershell
python scripts/upload_model_to_minio.py
```

Le script :

- attend que MinIO soit prêt
- crée le bucket s'il n'existe pas
- envoie `artifacts/models/model_latest.joblib`

## Démarrer l'application avec Docker Compose

```powershell
docker compose up -d --build
```

Services exposés :

- backend FastAPI : `http://localhost:8000`
- documentation API : `http://localhost:8000/docs`
- frontend Streamlit : `http://localhost:8501`
- console MinIO : `http://localhost:9001`

Identifiants MinIO locaux :

- utilisateur : `admin`
- mot de passe : `password123`

## Mise en route recommandée

1. installer les dépendances
2. copier `.env.example` vers `.env`
3. entraîner un modèle avec `python main.py`
4. démarrer Docker Compose
5. publier le modèle avec `python scripts/upload_model_to_minio.py`
6. vérifier `http://localhost:8000/health`
7. ouvrir `http://localhost:8501`
8. lancer une prédiction

## Faire une prédiction via l'API

### Exemple curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "median_income": 3.5,
    "housing_median_age": 20.0,
    "average_rooms": 5.0,
    "average_bedrooms": 1.0,
    "population": 1000.0,
    "average_occupancy": 3.0,
    "latitude": 34.0,
    "longitude": -118.0
  }'
```

### Réponse attendue

```json
{
  "prediction": 1.9648099999999993
}
```

La prédiction est exprimée en unite de `100 000 $`.

## Lancer le frontend sans Docker

```powershell
streamlit run frontend/streamlit_app.py
```

Si le backend n'est pas sur l'URL par défaut :

```powershell
$env:BACKEND_URL="http://127.0.0.1:8000"
streamlit run frontend/streamlit_app.py
```

## Tests et qualité

### Workflow local pre-push

Le script local principal est :

```powershell
powershell -ExecutionPolicy Bypass -File scripts\workflow_local.ps1
```

Mode correction automatique avant re-verification :

```powershell
powershell -ExecutionPolicy Bypass -File scripts\workflow_local.ps1 -Fix
```

Mode complet avec build, smoke tests Docker et scans d'images :

```powershell
powershell -ExecutionPolicy Bypass -File scripts\workflow_local.ps1 -Fix -WithDocker
```

Pour installer le hook `pre-push` du repo :

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_git_hook.ps1
```

Une fois installé, chaque `git push` lancera automatiquement le workflow local.

### Tests

```powershell
pytest -v --cov=src
```

### Lint

```powershell
ruff check .
```

### Formatage

```powershell
ruff format --check .
black --check .
```

### Securite

```powershell
bandit -r src/prediction/ src/common/ backend/ frontend/
```

## Logs et observabilité

Le code journalise les actions critiques :

- démarrage et arrêt du backend
- téléchargement du modèle depuis MinIO
- chargement en mémoire du modèle
- conversion du schema API vers le schéma du modèle
- exécution du pipeline d'entraînement
- upload vers MinIO
- appels du frontend vers l'API

Avec Docker :

```powershell
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f minio
```

## Depannage

### Erreur 422 sur `/predict`

Verifier :

- les noms de champs du JSON
- le type des valeurs envoyées

### Erreur 500 sur `/predict`

Vérifier :

- la présence du modèle dans MinIO
- les logs du backend
- la compatibilité entre le schéma API et le pipeline chargé

### Frontend inaccessible

Vérifier :

- `BACKEND_URL`
- `docker compose ps`
- `http://localhost:8000/health`

### Modèle absent dans MinIO

Exécuter :

```powershell
python main.py
python scripts/upload_model_to_minio.py
```

## Arrêter les services

```powershell
docker compose down
```

Pour supprimer aussi les volumes :

```powershell
docker compose down -v
```
