from pydantic import BaseModel, Field

"""Schema public accepte par l'API.
    Les noms sont explicites pour l'utilisateur final. Une couche de
    normalisation se charge ensuite de convertir ces champs vers les noms
    historiques attendus par le modele sklearn.
    """


class HousingFeatures(BaseModel):
    user_id: str = Field(
        "anonymous", description="Id utilisateur fictif pour le routage A/B"
    )
    median_income: float
    housing_median_age: float
    average_rooms: float
    average_bedrooms: float
    population: float
    average_occupancy: float
    latitude: float
    longitude: float
