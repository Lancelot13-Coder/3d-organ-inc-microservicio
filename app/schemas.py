"""
Esquemas Pydantic: definen la forma del JSON que el microservicio
entrega. FastAPI los usa para validar y para generar la documentación
automática en /docs.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Modelo3DOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = ""
    categoria: str
    fecha_registro: datetime
    activo: bool

    # Permite construir este schema directamente desde un objeto
    # SQLAlchemy (Modelo3D), no solo desde un dict.
    model_config = ConfigDict(from_attributes=True)
