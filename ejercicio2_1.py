import multiprocessing as mp

def cuadrado(x):
    p=mp.current_process()
    result = x * x
    print(f"pid:{p.pid} result:{result}")
    return result

if __name__ == '__main__':
    procesos = list()
    for i in range(10):
        p = mp.Process(target=cuadrado, args=(i+1,))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()


