from typing import List
from src.schemas.egresos import Egresos
from src.models.models import Egresos as EgresosModel

class EgresosRepository:
    def __init__(self, db):
        self.db = db

    def get_egresos(self, offset: int, limit: int) -> List[Egresos]:
        query = self.db.query(EgresosModel)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_egreso(self, id: int) -> Egresos:
        element = self.db.query(EgresosModel).filter(EgresosModel.id == id).first()
        return element

    def create_egreso(self, egreso: Egresos) -> Egresos:
        new_egreso = EgresosModel(**egreso.dict())
        self.db.add(new_egreso)
        self.db.commit()
        self.db.refresh(new_egreso)
        return new_egreso

    def delete_egreso(self, id: int) -> Egresos:
        element = self.db.query(EgresosModel).filter(EgresosModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def update_egreso(self, id: int, egreso: Egresos) -> Egresos:
        element = self.db.query(EgresosModel).filter(EgresosModel.id == id).first()

        element.date = egreso.date
        element.description = egreso.description
        element.value = egreso.value
        element.category = egreso.category
        self.db.commit()
        self.db.refresh(element)
        return element
