# Se importan los módulos necesarios
import sys
import psutil
import subprocess
import time

def ejecutar_proceso(nombre_proceso, comando):
    try:
        # Se inicia el proceso con el comando ingresado
        proceso = subprocess.Popen(comando.split())
        print(f"Proceso {nombre_proceso} iniciado")
        return proceso
    except Exception as error:
        # Si no se puede iniciar se imprime un mensaje de error
        print(f"Error al iniciar el proceso {nombre_proceso}: {error}")
        sys.exit(1)

def monitorear_proceso(nombre_proceso):
    # Se itera sobre todos los procesos en ejecución y revisa si alguno es nombre_proceso
    for proceso in psutil.process_iter(["pid", "name"]):
        if proceso.info["name"] == nombre_proceso:
            return True
    return False

if __name__ == "__main__":
    # Se revisa si el usuario ingresó la entrada correctamente
    if len(sys.argv) != 3:
        print("Debe ingresar: python3 monitoreo.py <nombre_del_proceso> <comando>")
        sys.exit(1)

    # Se obtiene el nombre del proceso y el comando para ejecutarlo
    nombre_proceso = sys.argv[1]
    comando = sys.argv[2]

    try:
        while True:
            # Se revisa si el proceso está en ejecución
            if monitorear_proceso(nombre_proceso):
                print(f"El proceso {nombre_proceso} está en ejecución.")
            else:
                # Si el proceso no está en ejecución se procede a iniciarlo
                print(f"El proceso {nombre_proceso} no está en ejecución. Iniciando...")
                proceso = ejecutar_proceso(nombre_proceso, comando)
            # Se espera 5 segundos y vuelve a revisar
            time.sleep(5)
    except KeyboardInterrupt:
        # Se detiene el programa al ingresar Ctrl + C
        print("\nPrograma finalizado por el usuario")
