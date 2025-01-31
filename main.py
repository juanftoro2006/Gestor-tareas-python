from tasks.task_manager import TaskManager

def mostrar_menu():
    print("\n=== Sistema de Gestión de Tareas ===")
    print("1. Crear una nueva tarea")
    print("2. Listar todas las tareas")
    print("3. Editar una tarea")
    print("4. Completar una tarea")
    print("5. Eliminar una tarea")
    print("6. Salir")

def obtener_entero(mensaje, minimo=1, maximo=None):
    """Solicita un número entero al usuario con validación."""
    while True:
        try:
            valor = int(input(mensaje))
            if maximo and not (minimo <= valor <= maximo):
                print(f"⚠️ El valor debe estar entre {minimo} y {maximo}.")
                continue
            return valor
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número válido.")

def main():
    gestor_tareas = TaskManager()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Ingrese el título de la tarea: ").strip()
            descripcion = input("Ingrese la descripción de la tarea: ").strip()
            fecha_limite = input("Ingrese la fecha límite (YYYY-MM-DD): ").strip()
            
            if not titulo or not descripcion or not fecha_limite:
                print("❌ Todos los campos son obligatorios.")
                continue
            
            try:
                gestor_tareas.crear_tarea(titulo, descripcion, fecha_limite)
                print("✅ Tarea creada con éxito.")
            except ValueError as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            tareas = gestor_tareas.listar_tareas()
            if tareas:
                print("\n=== Lista de Tareas ===")
                for idx, tarea in enumerate(tareas, 1):
                    print(f"{idx}. {tarea}")
            else:
                print("⚠️ No hay tareas registradas.")
        
        elif opcion == "3":
            if not gestor_tareas.tareas:
                print("⚠️ No hay tareas para editar.")
                continue
            id_tarea = obtener_entero("Ingrese el ID de la tarea que desea editar: ", maximo=len(gestor_tareas.tareas))
            nuevo_titulo = input("Ingrese el nuevo título (deje vacío para no cambiar): ").strip()
            nueva_descripcion = input("Ingrese la nueva descripción (deje vacío para no cambiar): ").strip()
            nueva_fecha_limite = input("Ingrese la nueva fecha límite (YYYY-MM-DD, deje vacío para no cambiar): ").strip()
            
            gestor_tareas.editar_tarea(id_tarea, nuevo_titulo, nueva_descripcion, nueva_fecha_limite)
            print("✅ Tarea actualizada con éxito.")
        
        elif opcion == "4":
            if not gestor_tareas.tareas:
                print("⚠️ No hay tareas para completar.")
                continue
            id_tarea = obtener_entero("Ingrese el ID de la tarea que desea marcar como completada: ", maximo=len(gestor_tareas.tareas))
            gestor_tareas.completar_tarea(id_tarea)
            print("✅ Tarea marcada como completada.")
        
        elif opcion == "5":
            if not gestor_tareas.tareas:
                print("⚠️ No hay tareas para eliminar.")
                continue
            id_tarea = obtener_entero("Ingrese el ID de la tarea que desea eliminar: ", maximo=len(gestor_tareas.tareas))
            gestor_tareas.eliminar_tarea(id_tarea)
            print("✅ Tarea eliminada con éxito.")
        
        elif opcion == "6":
            print("👋 ¡Gracias por usar el Sistema de Gestión de Tareas!")
            break
        
        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
