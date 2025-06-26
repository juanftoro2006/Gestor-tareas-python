# backend/app_api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tasks.task_manager import TaskManager

# 🔧 Crear instancia FastAPI
app = FastAPI()

# 🧠 Crear instancia única del gestor de tareas
gestor_tareas = TaskManager()

# 📦 Modelo de entrada para validación de datos
class TareaEntrada(BaseModel):
    titulo: str
    descripcion: str
    fecha_limite: str  # Formato esperado: "YYYY-MM-DD"

# 🌐 Configurar CORS para aceptar peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Puedes agregar más orígenes si lo necesitas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📋 GET /tareas - Obtener lista de tareas
@app.get("/tareas")
def obtener_tareas():
    tareas_serializadas = [
        {
            "id": i + 1,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "fecha_limite": tarea.fecha_limite.strftime("%Y-%m-%d"),
            "completada": tarea.completada,
            "creada_en": tarea.creada_en.isoformat(),
            "completada_en": tarea.completada_en.isoformat() if tarea.completada_en else None
        }
        for i, tarea in enumerate(gestor_tareas.tareas)
    ]
    return tareas_serializadas

# ➕ POST /tareas - Crear una nueva tarea
@app.post("/tareas")
def crear_tarea(tarea: TareaEntrada):
    try:
        gestor_tareas.crear_tarea(
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_limite=tarea.fecha_limite
        )
        return {"mensaje": "✅ Tarea creada correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
