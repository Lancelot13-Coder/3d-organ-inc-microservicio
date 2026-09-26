"""
Modelo SQLAlchemy que representa la tabla 'modelos' dentro de Supabase.

EJEMPLO: esta tabla representa lo mismo que 'Elemento' en tu proyecto
Django (catalogo/models.py), pero AQUÍ vive en una base de datos
distinta (Supabase / Postgres), separada del SQLite local de Django.
Simplificamos 'categoria' a un simple texto en vez de una relación
completa, para que el microservicio sea sencillo de empezar; puedes
convertirla en una tabla aparte con su propia relación más adelante.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from .database import Base


class Modelo3D(Base):
    __tablename__ = "modelos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True, default="")
    categoria = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
