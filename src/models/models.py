from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from src.config.database import Base

class Ingresos(Base):
    __tablename__ = "ingresos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    description = Column(String(length=100))
    value = Column(Float, index=True)
    category = Column(String(length=50), index=True)

class Egresos(Base):
    __tablename__ = "egresos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    description = Column(String(length=100))
    value = Column(Float, index=True)
    category = Column(String(length=50), index=True)

# Retorna las clases de modelos
def get_ingresos_model():
    return Ingresos

def get_egresos_model():
    return Egresos
