import multiprocessing as mp
import time

totalHijos = 1000

def hola (q,x):
    #time.sleep(1.0)
    #q.put("Hola desde " + str(mp.current_process().pid))
    msg=mp.current_process().pid,x,x*x
    q.put(msg)

if __name__ == '__main__':

    q = mp.Queue()
    procesos = list()

    for i in range(totalHijos):
        p = mp.Process(target=hola, args=(q,i))
        p.start()
        procesos.append(p)


    procesos[-1].join()

    cntr=0
    while not q.empty():
        cntr+=1
        msg = q.get()
        print(f"Padre ha recibido (cntr:{cntr}):", msg)
