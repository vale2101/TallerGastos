from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.repositories.ingresos import IngresosRepository
from src.repositories.egresos import EgresosRepository
from src.config.database import SessionLocal
from typing import Generator

report_router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@report_router.get('/reporte_basico', tags=['reportes'], description="Generates a basic expense report")
def basic_report(db: Session = Depends(get_db)) -> dict:
    ingresos_repo = IngresosRepository(db)
    egresos_repo = EgresosRepository(db)
    
    total_ingresos = sum(ingreso.value for ingreso in ingresos_repo.get_ingresos(0, None))
    total_egresos = sum(egreso.value for egreso in egresos_repo.get_egresos(0, None))
    diferencia = total_ingresos - total_egresos
    
    return {
        "total_ingresos": total_ingresos,
        "total_egresos": total_egresos,
        "diferencia": diferencia
    }

@report_router.get('/reporte_ampliado', tags=['reportes'], description="Generates an expanded expense report")
def expanded_report(db: Session = Depends(get_db)) -> dict:
    ingresos_repo = IngresosRepository(db)
    egresos_repo = EgresosRepository(db)
    
    ingresos_agrupados = {}
    for ingreso in ingresos_repo.get_ingresos(0, None):
        if ingreso.category in ingresos_agrupados:
            ingresos_agrupados[ingreso.category] += ingreso.value
        else:
            ingresos_agrupados[ingreso.category] = ingreso.value
    
    egresos_agrupados = {}
    for egreso in egresos_repo.get_egresos(0, None):
        if egreso.category in egresos_agrupados:
            egresos_agrupados[egreso.category] += egreso.value
        else:
            egresos_agrupados[egreso.category] = egreso.value
    
    return {
        "ingresos_agrupados": ingresos_agrupados,
        "egresos_agrupados": egresos_agrupados
    }
