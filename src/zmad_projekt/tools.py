""" 
Moduł zawiera narzędzia dla projektowanego Agenta AI

"""

# lub from . import functions
# lub from zmad_projekt_functions import calculate_stress
# from .functions import calculate_stress as calculate_stress_function

from pathlib import Path

from . import functions
from .schemas import Passenger
from .schemas import ConcreteSample

def calculate_stress(force: float, area: float) -> str:
    """ 
    This function takes the value of force in Newtons, 
    the area in square milimeters and returns the stress in [MPa].
    
    Args:
        force(float): Force in [N]
        area (float): Area in [mm^2]
    
    Returns: 
        str: The value of stress in [MPa] with description.
    """
    try:
        result = functions.calculate_stress(force, area)
        return f"value of stress is equal to {result:.2f} [MPa]."
    except ZeroDivisionError as e:
        return " You tried to divide by zero. Use positive values of the area"

def convert_temp(temperature_to_convert: float, output_unit: str) -> str:
    """ 
    This function takes temperature in Celsius and converts it to either Kelvin or Fahrenheit.
    
    Args:
        temperature_to_convert(float): temperature to convert
        output_unit(str): unit to convert to
    
    Returns: 
        str: converted temperature with unit label
    """
    try:
        result = functions.convert_(temperature_to_convert, output_unit)
        unit = output_unit.strip().upper()
        if unit in {"F", "FAHRENHEIT"}:
            unit_label = "F"
        elif unit in {"K", "KELVIN"}:
            unit_label = "K"
        else:
            unit_label = "C"

        return f"Converted temperature: {result:.2f} degrees {unit_label}."
    except ValueError:
        return "Unknown temperature unit. Try C, K, or F."


def predict_survival_on_titanic(
    Sex: str,
    Age: float,
    Pclass: int | None = None,
    SibSp: int | None = None,
    Parch: int | None = None,
    Fare: float | None = None,
    Embarked: str | None = None,
) -> str:
    """
    This function predicts, if the person with given
    attributes will have survived the Titanic crash

    Args:
        Sex (str): _description_
        Age (float): _description_
        Pclass (int | None, optional): _description_. Defaults to None.
        SibSp (int | None, optional): _description_. Defaults to None.
        Parch (int | None, optional): _description_. Defaults to None.
        Fare (float | None, optional): _description_. Defaults to None.
        Embarked (str | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    defaults: dict = {
        "Pclass": 3,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 50,
        "Embarked": "S",
    }

    sex_raw = Sex.strip().lower()
    if sex_raw in {"female", "woman", "f"}:
        sex_normalized = "female"
    elif sex_raw in {"male", "man", "m"}:
        sex_normalized = "male"
    else:
        return "Unknown Sex value. Use male/female (or man/woman)."

    embarked_normalized = (
        Embarked.strip().upper() if Embarked else defaults["Embarked"]
    )
    if embarked_normalized not in {"C", "Q", "S"}:
        embarked_normalized = defaults["Embarked"]
    
    passenger = Passenger(
        Sex=sex_normalized,
        Age=Age,
        Pclass=Pclass if Pclass is not None else defaults["Pclass"],
        SibSp=SibSp if SibSp is not None else defaults["SibSp"],
        Parch=Parch if Parch is not None else defaults["Parch"],
        Fare=Fare if Fare is not None else defaults["Fare"],
        Embarked=embarked_normalized,
        
    )

    model_path = Path(__file__).resolve().parents[1] / "models" / "titanic_rf_model.pkl"

    try:
        result = functions.predict_survival(
            model_path=model_path,
            passenger=passenger,
        )
    except Exception as e:
        return f"Prediction failed: {e}"
    
    if result:
        return "This passenger would have survived"
    else:
        return "This passenger would not have survived"




if __name__ == "__main__":
    area = 0
    force = 1850 * 9.81
    print(calculate_stress(force, area))
    
def predict_concrete_compressive_strength(
    cement: float,
    blast_furnace_slag: float,
    fly_ash: float,
    water: float,
    superplasticizer: float,
    coarse_aggregate: float,
    fine_aggregate: float,
    age: int
) -> str:
    """
    Predicts the concrete compressive strength in [MPa] based on component masses (per m^3) and age.
    
    Args:
        cement (float): Cement content [kg/m^3]
        blast_furnace_slag (float): Blast furnace slag content [kg/m^3]
        fly_ash (float): Fly ash content [kg/m^3]
        water (float): Water content [kg/m^3]
        superplasticizer (float): Superplasticizer content [kg/m^3]
        coarse_aggregate (float): Coarse aggregate content [kg/m^3]
        fine_aggregate (float): Fine aggregate content [kg/m^3]
        age (int): Age of testing in [days]
    """
    try:
        sample = ConcreteSample(
            cement=cement,
            blast_furnace_slag=blast_furnace_slag,
            fly_ash=fly_ash,
            water=water,
            superplasticizer=superplasticizer,
            coarse_aggregate=coarse_aggregate,
            fine_aggregate=fine_aggregate,
            age=age
        )
        model_path = Path(__file__).resolve().parents[1] / "models" / "concrete_regression_model.pkl"
        #model_file = Path("models/")
        predicted_strength = functions.predict_concrete_strength(model_path=model_path, sample=sample)
        
        return f"The predicted compressive strength of the concrete sample after {age} days is {predicted_strength:.2f} [MPa]."
    except Exception as e:
        return f"An error occurred during concrete strength prediction: {str(e)}"
