import multiprocessing as mp
import time

# Modificar el código cuadrado para que los hijos comuniquen al padre los resultados en forma de tupla: (pid , valor , cuadrado).

totalHijos=1000

def hola (q,x):
    time.sleep(1.0)
    print("Hola desde " + str(mp.current_process().pid))
    result= mp.current_process().pid, x, x*x
    q.put(result)

if __name__ == '__main__':

    q = mp.Queue()
    procesos = list()
    for i in range(totalHijos):
        p = mp.Process(target=hola, args=(q,i))
        p.start()
        procesos.append(p)

    procesos[0].join()
    cntr = 0
    while not q.empty():
        cntr +=1
        msg = q.get()
        print("Padre ha recibido:", msg)
    print(f"Padre ha recibido un total de {cntr} mensajes")