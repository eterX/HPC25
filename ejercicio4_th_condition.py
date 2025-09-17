import time
import numpy as np
import threading as thr
import multiprocessing as mp


ITERS = 100000
MAX_ITEMS = 4

def productor (l, cond):

    global valor

    name = thr.currentThread().getName()
    print("Thread {name} empezando.".format(name=name))

    for i in range(ITERS):
        cond.acquire()                      # Evalua condicion en EM
        while (len(l) == MAX_ITEMS):
            cond.wait()                     # Espera si se comple (libera EM)

        valor = valor + 1                   # Siguiente valor a la lista
        l.append(valor)

        cond.notifyAll()                    # Senializar a todos
        cond.release()                      # Dejar la RC


def consumidor (l, cond):

    name = thr.currentThread().getName()
    print("Thread {name} empezando.".format(name=name))

    for i in range(ITERS):
        cond.acquire()                      # Evaluar la condicion en EM
        while (len(l) == 0):
            cond.wait()                     # Espera si se cumple (libera EM)

        valor = l.pop(0)
        # print(name, " <- ", valor, len(l))

        cond.notifyAll()                    # Notificar a todos
        cond.release()                      # Dejar la RC



if __name__ == '__main__':

    P = mp.cpu_count()  # Num. processors/threads

    valor = 0

    cond = thr.Condition()
    lista = list()

    lista_t = list()
    for i in range(P):
        if (i % 2):
            t = thr.Thread(target = productor,  args=(lista, cond, ), name="PROD-"+str(i))
        else:
            t = thr.Thread(target = consumidor, args=(lista, cond, ), name="CONS-"+str(i))
        t.start()
        lista_t.append(t)

    for t in lista_t:
        t.join()

    print("Valor final: ", valor)
