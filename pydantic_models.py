import re
from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator

class PetIn(BaseModel):
    name: Annotated[str, Field(..., min_length=2, max_length=50, description="Кличка тварини", examples=["Рекс", "Сніжок"])]
    age: Annotated[str, Field(None, max_length=50, description="Вік тварини")]
    breed: Annotated[str, Field(..., min_length=2, max_length=50, description="Порода тварини")]
    notes: Annotated[str, Field(None, max_length=500, description="Примітки або додаткова інформація")]
    illness: Annotated[str, Field(None, max_length=50, description="Захворювання або стан")]


class PetOut(PetIn):
    id: str
