from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Modelos 3D (EJEMPLO)", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"servicio": "microservicio-modelos-3d", "estado": "ok"}


@app.get("/api/modelos", response_model=list[schemas.Modelo3DOut])
def listar_modelos(categoria: str | None = None, db: Session = Depends(get_db)):
    consulta = db.query(models.Modelo3D)
    if categoria:
        consulta = consulta.filter(models.Modelo3D.categoria == categoria)
    return consulta.all()


@app.get("/api/modelos/{modelo_id}", response_model=schemas.Modelo3DOut)
def obtener_modelo(modelo_id: int, db: Session = Depends(get_db)):
    modelo = db.query(models.Modelo3D).filter(models.Modelo3D.id == modelo_id).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo 3D no encontrado")
    return modelo


@app.post("/api/modelos", response_model=schemas.Modelo3DOut, status_code=201)
def crear_modelo(datos: schemas.Modelo3DCreate, db: Session = Depends(get_db)):
    nuevo = models.Modelo3D(**datos.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.put("/api/modelos/{modelo_id}", response_model=schemas.Modelo3DOut)
def editar_modelo(modelo_id: int, datos: schemas.Modelo3DUpdate, db: Session = Depends(get_db)):
    modelo = db.query(models.Modelo3D).filter(models.Modelo3D.id == modelo_id).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo 3D no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(modelo, campo, valor)
    db.commit()
    db.refresh(modelo)
    return modelo


@app.delete("/api/modelos/{modelo_id}", status_code=204)
def eliminar_modelo(modelo_id: int, db: Session = Depends(get_db)):
    modelo = db.query(models.Modelo3D).filter(models.Modelo3D.id == modelo_id).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo 3D no encontrado")
    db.delete(modelo)
    db.commit()
    return None