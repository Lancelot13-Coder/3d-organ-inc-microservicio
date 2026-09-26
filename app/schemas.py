from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Modelo3DOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = ""
    categoria: str
    fecha_registro: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class Modelo3DCreate(BaseModel):
    nombre: str
    descripcion: str | None = ""
    categoria: str
    activo: bool = True


class Modelo3DUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    activo: bool | None = None
