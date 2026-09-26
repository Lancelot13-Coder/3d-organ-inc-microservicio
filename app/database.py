"""
Conexión a la base de datos de Supabase (Postgres) usando SQLAlchemy.

DATABASE_URL se define como VARIABLE DE ENTORNO en Render (nunca la
escribas directamente aquí). Supabase te la da en:
    Project Settings -> Database -> Connection string -> URI

Tiene esta forma (EJEMPLO, no es una URL real):
    postgresql://postgres:TU_PASSWORD@db.xxxxxxxx.supabase.co:5432/postgres
"""

from dotenv import load_dotenv
load_dotenv()

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # EJEMPLO: mientras no configures la variable de entorno, usamos un
    # SQLite local (archivo microservicio.db) SOLO para poder levantar
    # el microservicio y probarlo sin depender todavía de Supabase.
    DATABASE_URL = "sqlite:///./microservicio.db"

# connect_args solo es necesario para SQLite (no molesta si usas Postgres
# en producción con Supabase, porque en ese caso DATABASE_URL ya no
# empieza con "sqlite").
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: abre una sesión de base de datos por
    petición y la cierra automáticamente al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
