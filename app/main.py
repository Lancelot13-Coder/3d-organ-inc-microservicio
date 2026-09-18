"""
Microservicio FastAPI (EJEMPLO) para 3D-Organ-Inc.

Este microservicio es INDEPENDIENTE del proyecto Django: se despliega
por separado (en Render) y su única función es exponer, vía HTTP/JSON,
los datos de la tabla 'modelos' que vive en Supabase.

Tu vista de Django (integracion/views.py) simplemente hace un
requests.get() a la URL pública de este servicio; no importa que esté
escrito en un lenguaje distinto (FastAPI/Python aquí, pero podría ser
cualquier otro).

Cómo correrlo en tu máquina para probarlo:
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8000

Documentación automática (interactiva) una vez corriendo:
    http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from . import models, schemas
from .database import Base, engine, get_db

# Crea la tabla 'modelos' automáticamente si no existe todavía
# (útil para SQLite local; en Supabase normalmente crearás la tabla
# tú mismo con el script schema.sql que se incluye en este proyecto).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Microservicio de Modelos 3D (EJEMPLO)",
    description="Expone los Modelos 3D guardados en Supabase para que Django los consuma.",
    version="1.0.0",
)

# CORS: permite que otros orígenes (ej. tu Django, o un navegador)
# puedan llamar a este microservicio. Para producción real, cambia
# allow_origins=["*"] por la URL exacta de tu app Django.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    """Endpoint simple para confirmar que el servicio está vivo."""
    return {"servicio": "microservicio-modelos-3d", "estado": "ok"}


@app.get("/api/modelos", response_model=list[schemas.Modelo3DOut])
def listar_modelos(categoria: str | None = None, db: Session = Depends(get_db)):
    """Lista todos los Modelos 3D. Si se pasa ?categoria=nombre en la
    URL, filtra por esa categoría (EJEMPLO de query param, igual que
    catalogo.views.por_categoria en Django, pero aquí vía HTTP)."""
    consulta = db.query(models.Modelo3D).filter(models.Modelo3D.activo == True)  # noqa: E712
    if categoria:
        consulta = consulta.filter(models.Modelo3D.categoria == categoria)
    return consulta.all()


@app.get("/api/modelos/{modelo_id}", response_model=schemas.Modelo3DOut)
def obtener_modelo(modelo_id: int, db: Session = Depends(get_db)):
    """Detalle de un Modelo 3D puntual (ruta dinámica, igual concepto
    que catalogo.views.detalle en Django, pero como endpoint HTTP)."""
    modelo = db.query(models.Modelo3D).filter(models.Modelo3D.id == modelo_id).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo 3D no encontrado")
    return modelo
