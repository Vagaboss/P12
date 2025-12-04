# tests/test_api.py
import sys
import os

# Ajoute la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app  # main.py de ton API

client = TestClient(app)


def test_predict_endpoint():
    payload = {
        "Region": "South",
        "Soil_Type": "Sandy",
        "Crop": "Rice",
        "Rainfall_mm": 500.0,
        "Temperature_Celsius": 28.0,
        "Fertilizer_Used": True,
        "Irrigation_Used": True,
        "Weather_Condition": "Sunny",
        "Days_to_Harvest": 120
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_yield" in data
    assert isinstance(data["predicted_yield"], float)


def test_recommend_endpoint():
    payload = {
        "Region": "South",
        "Soil_Type": "Sandy",
        "Rainfall_mm": 500.0,
        "Temperature_Celsius": 28.0,
        "Fertilizer_Used": True,
        "Irrigation_Used": True,
        "Weather_Condition": "Sunny",
        "Days_to_Harvest": 120
    }

    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0

    first = data["recommendations"][0]
    assert "Crop" in first
    assert "predicted_yield" in first
