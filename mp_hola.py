import multiprocessing as mp

x = 7


def hola ():
    global x
    x+=1
    print("Hello, world!", x) # Hello, world! 8



if __name__ == '__main__':

    p = mp.Process(target=hola, args=(), name="Hola")
    p.start()

    #x = 4

    p.join()
    print("x:", x)
    #Hello, world! 8
    #x: 7
    #porque son contextos disitntos
