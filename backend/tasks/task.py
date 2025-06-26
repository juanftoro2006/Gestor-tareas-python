from datetime import datetime

class Task:
    def __init__(self, titulo, descripcion, fecha_limite):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = self._convertir_fecha(fecha_limite)
        self.completada = False
        self.creada_en = datetime.now()
        self.completada_en = None

    def _convertir_fecha(self, fecha_str):
        """Convierte una cadena de fecha en un objeto datetime."""
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("⚠️ Formato de fecha inválido. Use YYYY-MM-DD.")

    def completar(self):
        """Marca la tarea como completada y guarda la fecha de finalización"""
        self.completada = True
        self.completada_en = datetime.now()

    def __str__(self):
        """Representación amigable de la tarea."""
        estado = "✅ completada" if self.completada else "❌ Pendiente"
        fecha_limite = self.fecha_limite.strftime('%Y-%m-%d') if self.fecha_limite else "Sin fecha"
        creada = self.creada_en.strftime('%Y-%m-%d %H:%M:%S')
        completada = (self.completada_en.strftime('%Y-%m-%d %H:%M:%S')if self.completada_en else "No completada")
        
        return (f"{estado} | {self.titulo}\nDescripción: {self.descripcion}\n"
                f"(Fecha Límite: {fecha_limite}\nCreada en:{creada}\nCompletada en: {completada}")
