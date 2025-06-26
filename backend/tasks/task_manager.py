import json
from datetime import datetime
from tasks.task import Task

class TaskManager:
    def __init__(self, archivo_datos="data/tasks.json"):
        self.archivo_datos = archivo_datos
        self.tareas = []
        self.cargar_tareas()

    def cargar_tareas(self):
        """Carga las tareas desde un archivo JSON."""
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                self.tareas = [
                    Task(
                        titulo=tarea["titulo"],
                        descripcion=tarea["descripcion"],
                        fecha_limite=tarea["fecha_limite"]
                    ) for tarea in datos
                ]
                for tarea, tarea_datos in zip(self.tareas, datos):
                    tarea.completada = tarea_datos["completada"]
                    tarea.creada_en = datetime.fromisoformat(tarea_datos["creada_en"])
                    tarea.completada_en = datetime.fromisoformat(tarea_datos["completada_en"]) if tarea_datos["completada_en"] else None
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Error al cargar tareas: {e}")
            self.tareas = []

    def guardar_tareas(self):
        """Guarda las tareas en un archivo JSON."""
        datos = [
            {
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "fecha_limite": tarea.fecha_limite.strftime("%Y-%m-%d") if tarea.fecha_limite else None,
                "completada": tarea.completada,
                "creada_en": tarea.creada_en.isoformat(),
                "completada_en": tarea.completada_en.isoformat() if tarea.completada_en else None
            } for tarea in self.tareas
        ]
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)

    def crear_tarea(self, titulo, descripcion, fecha_limite):
        """Crea una nueva tarea y la añade a la lista."""
        tarea = Task(titulo, descripcion, fecha_limite)
        self.tareas.append(tarea)
        self.guardar_tareas()
        print("✅ Tarea creada correctamente.")

    def listar_tareas(self):
        """Devuelve una lista con todas las tareas."""
        return self.tareas if self.tareas else print("⚠️ No hay tareas registradas.")

    def editar_tarea(self, id_tarea, nuevo_titulo=None, nueva_descripcion=None, nueva_fecha_limite=None):
        """Edita una tarea existente."""
        if not (1 <= id_tarea <= len(self.tareas)):
            print("⚠️ ID de tarea inválido.")
            return

        tarea = self.tareas[id_tarea - 1]
        if nuevo_titulo:
            tarea.titulo = nuevo_titulo
        if nueva_descripcion:
            tarea.descripcion = nueva_descripcion
        if nueva_fecha_limite:
            tarea.fecha_limite = tarea._convertir_fecha(nueva_fecha_limite)
        self.guardar_tareas()
        print("✅ Tarea editada correctamente.")

    def completar_tarea(self, id_tarea):
        """Marca una tarea como completada."""
        if not (1 <= id_tarea <= len(self.tareas)):
            print("⚠️ ID de tarea inválido.")
            return

        self.tareas[id_tarea - 1].completar()
        self.guardar_tareas()
        print("✅ Tarea marcada como completada.")

    def eliminar_tarea(self, id_tarea):
        """Elimina una tarea de la lista."""
        if not (1 <= id_tarea <= len(self.tareas)):
            print("⚠️ ID de tarea inválido.")
            return

        self.tareas.pop(id_tarea - 1)
        self.guardar_tareas()
        print("✅ Tarea eliminada correctamente.")