import multiprocessing as mp
import time

SIZE = 16

def cuadrado(x):
    return x*x

def datos_generador():
    for i in range(SIZE):
        yield i

if __name__ == '__main__':

   # with mp.Pool(processes=4) as pool:
   #    res = pool.map(cuadrado, datos_generador())
   #
   # TODO: probar imap()
   #
   res = mp.Pool().map(cuadrado, datos_generador())
   print("Resultado:", res)
