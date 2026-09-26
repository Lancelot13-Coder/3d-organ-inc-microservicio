# Microservicio de Modelos 3D (FastAPI + Supabase + Render)

Este es un proyecto **separado** de tu Django (3D-Organ-Inc). Su único
trabajo es leer la tabla `modelos` desde Supabase y entregarla como
JSON por HTTP, para que tu vista `integracion/views.py` (en Django) la
consuma con `requests.get()`.

```
GitHub (este código)
    -> Render (lo descarga y lo corre 24/7)
        -> Supabase (Postgres en la nube, la base de datos real)
    <- responde JSON en /api/modelos
Django (integracion/views.py) -> le pide datos a la URL de Render
```

## 1. Probarlo en tu máquina primero (sin Supabase todavía)

```bash
cd microservicio_render
python -m venv venv
# Windows: venv\Scripts\Activate.ps1  (o activate.bat / usa cmd si PowerShell bloquea)
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Como no configuraste `DATABASE_URL` todavía, usará automáticamente un
SQLite local (`microservicio.db`) solo para que puedas ver que
funciona. Visita:

- `http://127.0.0.1:8000/` — confirma que el servicio está vivo
- `http://127.0.0.1:8000/docs` — documentación interactiva (puedes probar los endpoints desde ahí)
- `http://127.0.0.1:8000/api/modelos` — lista vacía al principio (SQLite local nuevo, sin datos)

## 2. Crear el proyecto en Supabase

1. Ve a https://supabase.com/ y crea una cuenta / inicia sesión.
2. Crea un **New Project** (elige una contraseña de base de datos y guárdala, la necesitarás).
3. Una vez creado, ve a **SQL Editor** (menú izquierdo) → **New query**.
4. Pega el contenido del archivo `schema.sql` de esta carpeta y ejecútalo (botón Run). Esto crea la tabla `modelos` con 2 registros de ejemplo.
5. Ve a **Project Settings** (ícono de engranaje) → **Database** → **Connection string** → pestaña **URI**. Copia esa URL; se ve así (con tu contraseña real en vez de `TU_PASSWORD`):
   ```
   postgresql://postgres:TU_PASSWORD@db.xxxxxxxx.supabase.co:5432/postgres
   ```
   

## 3. Probar el microservicio contra Supabase (todavía en tu máquina)

1. Copia `.env.example` como `.env` y pega ahí tu connection string real.
2. Instala `python-dotenv` (ya está en `requirements.txt`) y agrega esta línea al inicio de `app/database.py` si quieres que lea el `.env` automáticamente:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
3. Corre de nuevo `uvicorn app.main:app --reload --port 8000` y visita `http://127.0.0.1:8000/api/modelos` — ahora deberías ver los 2 registros de ejemplo que insertó `schema.sql`, viniendo de Supabase.

## 4. Subir este microservicio a GitHub

Este código debe vivir en **su propio repositorio** (o al menos su propia carpeta clara), separado del repositorio de tu proyecto Django, para que Render sepa exactamente qué desplegar.

```bash
cd microservicio_render
git init
git add .
git commit -m "Microservicio FastAPI inicial"
```

Crea un repositorio nuevo y vacío en GitHub (ej. `3d-organ-inc-microservicio`) y luego:

```bash
git remote add origin https://github.com/TU_USUARIO/3d-organ-inc-microservicio.git
git branch -M main
git push -u origin main
```

## 5. Desplegar en Render, conectado a ese repositorio de GitHub

1. Ve a https://render.com/ y crea una cuenta / inicia sesión (puedes usar "Sign in with GitHub").
2. Dashboard → **New** → **Web Service**.
3. Conecta tu cuenta de GitHub si no lo has hecho, y selecciona el repositorio `3d-organ-inc-microservicio`.
4. Configura:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. En la sección **Environment Variables**, agrega:
   - `DATABASE_URL` = tu connection string real de Supabase (la misma del paso 2).
6. Dale a **Create Web Service**. Render clona tu repo, instala dependencias y lo levanta. Al terminar, te da una URL pública como:
   ```
   https://tu-microservicio.onrender.com
   ```
7. Prueba `https://tu-microservicio.onrender.com/api/modelos` desde el navegador — deberías ver el mismo JSON que viste en local, ahora servido desde la nube.

> Cada vez que hagas `git push` a `main`, Render vuelve a desplegar automáticamente (eso es "conectado a GitHub": no tienes que subir nada manualmente a Render).

## 6. Conectar esto con tu proyecto Django

Ya tienes todo el lado Django listo (`integracion/views.py`). Solo falta apuntarlo a la URL real:

- **Opción A (recomendada), variable de entorno:**
  ```bash
  # antes de correr manage.py runserver
  # Windows (PowerShell):
  $env:MICROSERVICIO_URL="https://tu-microservicio.onrender.com/api/modelos"
  # macOS/Linux:
  export MICROSERVICIO_URL="https://tu-microservicio.onrender.com/api/modelos"
  ```
- **Opción B, directo en el código:** edita el valor por defecto en `config/settings.py`, variable `MICROSERVICIO_URL`.

Visita `http://127.0.0.1:8000/microservicio/` en tu Django — ahora debería mostrarte los datos reales que vienen desde Supabase, a través de Render.

## Notas

- El endpoint devuelve una **lista** de modelos (`/api/modelos`) o **uno solo** (`/api/modelos/5`). La vista actual de Django (`integracion/views.py`) simplemente imprime el JSON crudo; cuando tengas esto funcionando, dime y adaptamos ese template para mostrarlo como tarjetas/lista en vez de JSON crudo.
- Esta tabla `modelos` en Supabase es independiente de tu tabla `Elemento` en SQLite (Django). Son dos bases de datos distintas a propósito, para ilustrar justo lo que pediste: un microservicio con su propia base en la nube.
