from fastapi import APIRouter, Body, Path, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from src.schemas.egresos import Egresos
from src.repositories.egresos import EgresosRepository
from src.config.database import SessionLocal
from typing import Generator

egresos_router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@egresos_router.get('/egreso',
                    tags=['egresos'],
                    response_model=List[Egresos],
                    description="Returns all egresos stored")
def get_all_egresos(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Egresos]:
    return EgresosRepository(db).get_egresos(offset, limit)

@egresos_router.get('/egreso/{id}',
                    tags=['egresos'],
                    response_model=Egresos,
                    description="Returns data of one specific egreso")
def get_egreso(id: int = Path(..., title="The ID of the egreso to get", ge=1),
               db: Session = Depends(get_db)) -> Egresos:
    egreso = EgresosRepository(db).get_egreso(id)
    if not egreso:
        return JSONResponse(content={
            "message": "The requested egreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return egreso

@egresos_router.post('/egreso',
                     tags=['egresos'],
                     response_model=Egresos,
                     description="Creates a new egreso")
def create_egreso(egreso: Egresos = Body(...), db: Session = Depends(get_db)) -> Egresos:
    return EgresosRepository(db).create_egreso(egreso)

@egresos_router.put('/egreso/{id}',
                     tags=['egresos'],
                     response_model=Egresos,
                     description="Updates the data of specific egreso")
def update_egreso(id: int = Path(..., title="The ID of the egreso to update", ge=1),
                  egreso: Egresos = Body(...), db: Session = Depends(get_db)) -> Egresos:
    updated_egreso = EgresosRepository(db).update_egreso(id, egreso)
    if not updated_egreso:
        return JSONResponse(content={
            "message": "The requested egreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return updated_egreso

@egresos_router.delete('/egreso/{id}',
                       tags=['egresos'],
                       response_model=Egresos,
                       description="Removes specific egreso")
def remove_egreso(id: int = Path(..., title="The ID of the egreso to remove", ge=1),
                  db: Session = Depends(get_db)) -> Egresos:
    removed_egreso = EgresosRepository(db).delete_egreso(id)
    if not removed_egreso:
        return JSONResponse(content={
            "message": "The requested egreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return removed_egreso
