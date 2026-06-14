from pydantic import BaseModel


class Passenger(BaseModel):
    """Model danych pasażera"""
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    
    
class ConcreteSample(BaseModel):
    """Model danych próbki betonu"""
    cement: float
    blast_furnace_slag: float
    fly_ash: float
    water: float
    superplasticizer: float
    coarse_aggregate: float
    fine_aggregate: float
    age: int
