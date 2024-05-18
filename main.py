from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.routers.egresos import egresos_router
from src.routers.ingresos import ingresos_router
from src.routers.reportes import report_router
from src.config.database import Base, engine
from src.routers.auth import auth_router

#################################################
app = FastAPI()
app.title = "Taller Gastos "
app.summary = "Taller gastos usando fastApi"
app.description = "This is a demonstration of API REST using Python"
app.version = "0.0.2"
app.contact = {
    "name": "Valeria Herrera Parra - Katherin Castaño",
    "email": "valeria.herrerap@autonoma.edu.co",
}
#################################################
app.openapi_tags = [
    {
        "name": "reportes",
        "description": "Expense report endpoints",
    },
    {
    "name": "auth",
    "description": "User's authentication",
    },
]
#################################################
## Middlewares
app.add_middleware(ErrorHandler)
#################################################

## Router's definition (endpoints sets)
app.include_router(router=ingresos_router)
app.include_router(router=egresos_router)
app.include_router(router=report_router)
#################################################

Base.metadata.create_all(bind=engine)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

