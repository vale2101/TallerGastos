from typing import List
from src.schemas.ingresos import Ingresos
from src.models.models import Ingresos as IngresosModel

class IngresosRepository:
    def __init__(self, db):
        self.db = db

    def get_ingresos(self, offset: int, limit: int) -> List[Ingresos]:
        query = self.db.query(IngresosModel)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_ingreso(self, id: int) -> Ingresos:
        element = self.db.query(IngresosModel).filter(IngresosModel.id == id).first()
        return element

    def create_ingreso(self, ingreso: Ingresos) -> Ingresos:
        new_ingreso = IngresosModel(**ingreso.dict())
        self.db.add(new_ingreso)
        self.db.commit()
        self.db.refresh(new_ingreso)
        return new_ingreso

    def delete_ingreso(self, id: int) -> Ingresos:
        element = self.db.query(IngresosModel).filter(IngresosModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def update_ingreso(self, id: int, ingreso: Ingresos) -> Ingresos:
        element = self.db.query(IngresosModel).filter(IngresosModel.id == id).first()

        element.date = ingreso.date
        element.description = ingreso.description
        element.value = ingreso.value
        element.category = ingreso.category
        self.db.commit()
        self.db.refresh(element)
        return element
