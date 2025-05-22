from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session
import uvicorn

from models import Pet, get_db
from pydantic_models import PetIn, PetOut

app = FastAPI(
    title="PetCare API",
    description="Сервіс обліку тварин, які перебувають під наглядом ветеринарів.",
    version="1.0.1"
)

@app.post("/patients/", tags=["Пацієнти"], summary="Зареєструвати нового пацієнта", status_code=status.HTTP_201_CREATED, response_model=PetOut)
async def register_pet(pet: PetIn, db: Session = Depends(get_db)):
    new_pet = Pet(**pet.model_dump(), id=uuid4().hex)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

@app.get("/patients/", tags=["Пацієнти"], summary="Отримати список усіх пацієнтів", response_model=list[PetOut])
async def list_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()

@app.get("/patients/{pet_id}", tags=["Пацієнти"], summary="Дані конкретного пацієнта", response_model=PetOut)
async def get_pet(pet_id: str = Path(..., description="Ідентифікатор пацієнта"), db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пацієнта не знайдено")
    return pet

@app.delete("/patients/{pet_id}", tags=["Пацієнти"], summary="Видалити пацієнта", status_code=status.HTTP_200_OK)
async def remove_pet(pet_id: str = Path(..., description="Ідентифікатор пацієнта"), db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пацієнта не знайдено")
    db.delete(pet)
    db.commit()
    return {"msg": "Пацієнт успішно видалений"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
