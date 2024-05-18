from fastapi import APIRouter, Body, Path, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Generator, List
from src.schemas.ingresos import Ingresos
from src.repositories.ingresos import IngresosRepository
from src.config.database import SessionLocal

ingresos_router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@ingresos_router.get('/ingreso',
                     tags=['ingresos'],
                     response_model=List[Ingresos],
                     description="Returns all ingresos stored")
def get_all_ingresos(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Ingresos]:
    return IngresosRepository(db).get_ingresos(offset, limit)

@ingresos_router.get('/ingreso/{id}',
                     tags=['ingresos'],
                     response_model=Ingresos,
                     description="Returns data of one specific ingreso")
def get_ingreso(id: int = Path(..., title="The ID of the ingreso to get", ge=1),
                db: Session = Depends(get_db)) -> Ingresos:
    ingreso = IngresosRepository(db).get_ingreso(id)
    if not ingreso:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return ingreso

@ingresos_router.post('/ingreso',
                      tags=['ingresos'],
                      response_model=Ingresos,
                      description="Creates a new ingreso")
def create_ingreso(ingreso: Ingresos = Body(...), db: Session = Depends(get_db)) -> Ingresos:
    return IngresosRepository(db).create_ingreso(ingreso)

@ingresos_router.put('/ingreso/{id}',
                     tags=['ingresos'],
                     response_model=Ingresos,
                     description="Updates the data of specific ingreso")
def update_ingreso(id: int = Path(..., title="The ID of the ingreso to update", ge=1),
                   ingreso: Ingresos = Body(...), db: Session = Depends(get_db)) -> Ingresos:
    updated_ingreso = IngresosRepository(db).update_ingreso(id, ingreso)
    if not updated_ingreso:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return updated_ingreso

@ingresos_router.delete('/ingreso/{id}',
                        tags=['ingresos'],
                        response_model=Ingresos,
                        description="Removes specific ingreso")
def remove_ingreso(id: int = Path(..., title="The ID of the ingreso to remove", ge=1),
                   db: Session = Depends(get_db)) -> Ingresos:
    removed_ingreso = IngresosRepository(db).delete_ingreso(id)
    if not removed_ingreso:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return removed_ingreso
