from scipy.constants import value
import math as m
import numpy as np
import pandas as pd
from pathlib import Path
import joblib

from zmad_projekt.schemas import Passenger
from zmad_projekt.schemas import ConcreteSample

def calculate_stress(force: float, area: float) -> float: 
    return force / area

def predict_survival(model_path: str | Path, passenger: Passenger) -> bool:
    model = joblib.load(model_path)
    passenger_df = pd.DataFrame([passenger.model_dump()])
    prediction = model.predict(passenger_df)[0]
    return bool(prediction)

# if __name__ == "__main__":
#     area = m.pi * 100 / 4
#     force = 1850 * 9.81
#     print(calculate_stress(force, area))

def convert_(temperature_to_convert: float, output_unit: str) -> float:
    unit = output_unit.strip().upper()

    if unit in {"F", "FAHRENHEIT"}:
        return (temperature_to_convert * 9 / 5) + 32
    if unit in {"K", "KELVIN"}:
        return temperature_to_convert + 273.15
    if unit in {"C", "CELSIUS"}:
        return temperature_to_convert

    raise ValueError("Unknown unit")

def predict_concrete_strength(model_path: str | Path, sample: ConcreteSample) -> float:
    """Wczytuje model RandomForestRegressor i przewiduje wytrzymałość betonu w MPa"""
    model = joblib.load(model_path)
    sample_df = pd.DataFrame([sample.model_dump()])
    prediction = model.predict(sample_df)[0]
    return float(prediction)
    