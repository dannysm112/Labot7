# Se importan los módulos necesarios
import sys
import psutil

def obtener_informacion_proceso(id):
    try:
        # Se intenta obtener información sobre el proceso con el ID ingresado
        proceso = psutil.Process(id)

        # Se obtienen los datos solicitados sobre el proceso
        nombre = proceso.name()
        pid = proceso.pid
        parent_id = proceso.ppid()
        propietario = proceso.username()
        porcentaje_cpu = proceso.cpu_percent()
        consumo_memoria = proceso.memory_info().rss
        estado = proceso.status()
        path_ejecutable = proceso.exe()

        # Se devuelve un diccionario con la información
        return {
            "Nombre del proceso": nombre,
            "ID del proceso": pid,
            "Parent process ID": parent_id,
            "Usuario propietario": propietario,
            "Porcentaje de uso de CPU": porcentaje_cpu,
            "Consumo de memoria": consumo_memoria,
            "Estado": estado,
            "Path del ejecutable": path_ejecutable
        }

    except psutil.NoSuchProcess:
        # Si el proceso no se encontró se retorna un mensaje de error
        return f"No se encontró un proceso con el ID {id}"

# Se revisa si el script se está ejecutando como programa principal
if __name__ == "__main__":
    # Se revisa si el usuario ingresó la entrada correctamente
    if len(sys.argv) != 2:
        print("Debe ingresar: python3 informacion.py <ID_del_proceso>")
        sys.exit(1)
    
    try:
        # Se obtiene la información del proceso con el ID ingresado
        id = int(sys.argv[1])
        informacion = obtener_informacion_proceso(id)
    except ValueError:
        # Si el ID ingresado no es un número se imprime un mensaje de error
        print("El ID ingresado no es válido")
        sys.exit(1)

    # Se revisa si la información es un string (por lo cual hubo un error)
    if isinstance(informacion, str):
        # Se muestra el mensaje de error
        print(informacion)
    else:
        # Se muestra la información del proceso
        for dato, valor in informacion.items():
            print(f"{dato}: {valor}")
