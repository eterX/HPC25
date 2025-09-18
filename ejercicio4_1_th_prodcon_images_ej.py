import threading as thr
import cv2
import os
import time
import multiprocessing as mp

folder_in  = os.path.join("..", "data", "image_set", "input_th")
folder_out = os.path.join("..", "data", "image_set", "output_th")
os.makedirs(folder_out, exist_ok=True)


# --- PRODUCTOR ---
def productor(cond):
    global terminado
    nombre = thr.current_thread().name
    # Pasos a seguir:
    # 1. Recorrer todos los archivos de la carpeta de entrada.
    # 3. Para cada archivo:
    #     a. Esperar si el buffer está lleno.
    #     b. Leer la imagen del archivo.
    #     c. Añadir la imagen al buffer.
    #     d. Avisar a los consumidores que hay datos disponibles.
    # 4. Marcar que se ha terminado de producir y avisar a los consumidores.

# --- CONSUMIDOR ---
def consumidor(cond):
    global terminado
    nombre = thr.current_thread().name
    # Pasos a seguir:
    # 1. Mientras haya trabajo:
    #     a. Esperar si el buffer está vacío y no se ha terminado.
    #     b. Salir si el buffer está vacío y la producción ha terminado.
    #     c. Sacar una imagen del buffer.
    #     d. Avisar a otros hilos de cambios en el buffer.
    # 3. Procesar la imagen:
    #     a. Convertir la imagen a escala de grises.
    #           gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     b. Guardar la imagen procesada en la carpeta de salida.
    #           outpath = os.path.join(folder_out, f"gray_{fname}")
    #           cv2.imwrite(outpath, gray)
    #     c. Simular tiempo de procesamiento.
    #           time.sleep(1)  # simular procesamiento lento


# --- MAIN ---
if __name__ == "__main__":
    BUFFER_SIZE = 3
    buffer = []
    cond = thr.Condition()
    terminado = False   # flag global para señalizar fin de producción
    
    P = mp.cpu_count()  # número de hilos totales
    lista_t = []

    t = thr.Thread(target=productor, args=(cond,), name="PROD")
    lista_t.append(t)

    for i in range(P):
        t = thr.Thread(target=consumidor, args=(cond,), name="CONS-"+str(i)) # consumidores
        t.start()
        lista_t.append(t)

    for t in lista_t:
        t.join()

    print("Procesamiento terminado.")
