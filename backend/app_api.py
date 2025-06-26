# backend/app_api.py
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tasks.task_manager import TaskManager

app = FastAPI()
gestor_tareas = TaskManager()

# Modelo de entrada para nuevas tareas
class TareaEntrada(BaseModel):
    titulo: str
    descripcion: str
    fecha_limite: str

@app.get("/tareas")
def obtener_tareas():
    return [
        {
            "titulo": t.titulo,
            "descripcion": t.descripcion,
            "fecha_limite": t.fecha_limite.strftime("%Y-%m-%d"),
            "completada": t.completada,
            "creada_en": t.creada_en.isoformat(),
            "completada_en": t.completada_en.isoformat() if t.completada_en else None
        }
        for t in gestor_tareas.listar_tareas()
    ]

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


# 🔓 Permitir peticiones desde el frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tareas")
def obtener_tareas():
    """Devuelve todas las tareas registradas"""
    return [
        {
            "id": i + 1,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "fecha_limite": tarea.fecha_limite.strftime("%Y-%m-%d"),
            "completada": tarea.completada
        }
        for i, tarea in enumerate(gestor_tareas.tareas)
    ]

@app.post("/tareas")
def crear_tarea(tarea: dict):
    """Recibe una nueva tarea y la guarda"""
    gestor_tareas.crear_tarea(
        tarea["titulo"],
        tarea["descripcion"],
        tarea["fecha_limite"]
    )
    return {"mensaje": "✅ Tarea creada con éxito"}
