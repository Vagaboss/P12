from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib

# ---------- Chargement du modèle au démarrage ----------

MODEL_PATH = "models/best_linear_regression.joblib"
model = joblib.load(MODEL_PATH)

# Liste des cultures possibles (à adapter à ton dataset si besoin)
POSSIBLE_CROPS = ["Barley", "Cotton", "Maize", "Rice", "Soybean", "Wheat"]

# ---------- Schémas Pydantic ----------

class PredictInput(BaseModel):
    Region: str
    Soil_Type: str
    Crop: str
    Rainfall_mm: float
    Temperature_Celsius: float
    Fertilizer_Used: bool
    Irrigation_Used: bool
    Weather_Condition: str
    Days_to_Harvest: int


class PredictOutput(BaseModel):
    predicted_yield: float


class RecommendInput(BaseModel):
    Region: str
    Soil_Type: str
    Rainfall_mm: float
    Temperature_Celsius: float
    Fertilizer_Used: bool
    Irrigation_Used: bool
    Weather_Condition: str
    Days_to_Harvest: int


class Recommendation(BaseModel):
    Crop: str
    predicted_yield: float


class RecommendOutput(BaseModel):
    recommendations: List[Recommendation]


# ---------- Initialisation de l'app FastAPI ----------

app = FastAPI(
    title="Agritech Answers - Crop Yield API",
    description="API de prédiction et recommandation de rendements agricoles",
    version="1.0.0",
)


# ---------- Endpoint /predict ----------

@app.post("/predict", response_model=PredictOutput)
def predict_yield(payload: PredictInput):
    """
    Prend en entrée les infos d'une parcelle + culture,
    retourne le rendement prédit (t/ha).
    """
    # Conversion en DataFrame
    data = pd.DataFrame([payload.dict()])

    # Prédiction
    y_pred = model.predict(data)[0]

    return PredictOutput(predicted_yield=float(y_pred))


# ---------- Endpoint /recommend ----------

@app.post("/recommend", response_model=RecommendOutput)
def recommend_crop(payload: RecommendInput):
    """
    Prend en entrée le contexte de la parcelle (sans culture),
    teste toutes les cultures possibles et retourne un classement
    par rendement décroissant.
    """
    base_data = payload.dict()

    rows = []
    for crop in POSSIBLE_CROPS:
        row = base_data.copy()
        row["Crop"] = crop
        rows.append(row)

    df = pd.DataFrame(rows)

    y_preds = model.predict(df)

    results = []
    for crop, y in zip(POSSIBLE_CROPS, y_preds):
        results.append(
            Recommendation(
                Crop=crop,
                predicted_yield=float(y)
            )
        )

    # Tri décroissant par rendement
    results_sorted = sorted(results, key=lambda x: x.predicted_yield, reverse=True)

    return RecommendOutput(recommendations=results_sorted)
