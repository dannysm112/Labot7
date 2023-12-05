# Se importan los módulos necesarios
import sys
import psutil
import subprocess
import time
import matplotlib.pyplot as plt

# Función para ejecutar el binario y obtener el proceso
def ejecutar_binario(binario):
    try:
        proceso = subprocess.Popen(binario)
        print(f"Ejecutando el binario: {binario}")
        return proceso
    except Exception as error:
        # Si no se puede ejecutar se imprime un mensaje de error
        print(f"Error al ejecutar {binario}: {error}")
        sys.exit(1)

# Función para registrar el consumo de CPU y memoria en el archivo de log
def registrar_consumo(pid, archivo_log):
    try:

        # Se obtienen los datos a ingresar en el archivo
        proceso = psutil.Process(pid)
        tiempo = time.time()
        porcentaje_cpu = proceso.cpu_percent()
        consumo_memoria = proceso.memory_info().rss

        # Se escribe la info en el archivo de log
        with open(archivo_log, "a") as file:
            file.write(f"{tiempo},{porcentaje_cpu},{consumo_memoria}\n")

    except psutil.NoSuchProcess:
        print(f"No se encontró el proceso ingresado")
        sys.exit(1)

# Función para graficar el consumo de CPU y memoria
def graficar_consumo(archivo_log):
    datos = {"tiempo": [], "cpu": [], "memoria": []}

    # Se leen los datos del archivo de log 
    with open(archivo_log, "r") as file:
        for linea in file:
            tiempo, cpu, memoria = map(float, linea.strip().split(','))
            datos["tiempo"].append(tiempo)
            datos["cpu"].append(cpu)
            datos["memoria"].append(memoria)

    # Se genera la gráfica con los datos usando matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(datos["tiempo"], datos["cpu"], label="Consumo de CPU (%)")
    plt.plot(datos["tiempo"], datos["memoria"], label="Consumo de memoria (bytes)")
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Consumo")
    plt.legend()
    plt.title("Consumo de CPU y Memoria")
    plt.show()

if __name__ == "__main__":
    # Se revisa si el usuario ingresó la entrada correctamente
    if len(sys.argv) != 2:
        print("Debe ingresar: python3 consumo.py <ruta_del_ejecutable>")
        sys.exit(1)

    # Se obtiene la ruta del ejecutable y se le da nombre al archivo
    ruta_ejecutable = sys.argv[1]
    archivo_log = "registro_consumo.log"

    # Se ejecuta y se obtiene el proceso
    proceso = ejecutar_binario(ruta_ejecutable)

    try:
        # (Según la documentación que busqué) el método .poll revisa si el proceso ya se detuvo
        while proceso.poll() is None:
            registrar_consumo(proceso.pid, archivo_log)
            time.sleep(1)

    except KeyboardInterrupt:
        # Se detiene el programa al ingresar Ctrl + C
        print("\nPrograma finalizado por el usuario")

    finally:
        # Se finaliza el proceso y se espera a que termine
        print("Finalizando proceso...")
        proceso.terminate()
        proceso.wait()
        print("Proceso finalizado")

    # Se grafica el consumo de CPU y memoria usando el archivo de log
    graficar_consumo(archivo_log)
