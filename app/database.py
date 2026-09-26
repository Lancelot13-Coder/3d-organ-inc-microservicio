"""
Conexión a la base de datos de Supabase (Postgres) usando SQLAlchemy.

DATABASE_URL se define como VARIABLE DE ENTORNO en Render (nunca la
escribas directamente aquí). Supabase te la da en:
    Project Settings -> Database -> Connection string -> URI

Tiene esta forma (EJEMPLO, no es una URL real):
    postgresql://postgres:TU_PASSWORD@db.xxxxxxxx.supabase.co:5432/postgres
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./microservicio.db"

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # connect_timeout: si no logra conectar en 10 segundos, falla YA
    # con un error claro, en vez de quedarse colgado indefinidamente.
    connect_args = {"connect_timeout": 10}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

