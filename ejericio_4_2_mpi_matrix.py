from mpi4py import MPI
import numpy as np
import time

#globales
DEBUG=False #TODO: sacar del entorno o del debugger...
maxMatrizElementos = 1000  # para la verificación

if __name__ == '__main__':


    if DEBUG:
        rank = 0
        P = 4
        class MPItrucho:
            def __init__(self, rank, P):
                self.rank = rank
                self.P = P
            def Get_rank(self):
                return self.rank
            def Get_size(self):
                return self.P
            def send(self, *args, **kwargs):
                #print(f"DEBUG: Rank:{self.rank} enviando a {dest}: {data}")
                print(f"DEBUG: Rank:{self.rank}.send({args},{kwargs})")
            def recv(self, source, status):
                data = list(range(COLS))
                print(f"DEBUG: Rank:{self.rank} recibiendo de {source}: {data}")
                return data
        comm = MPItrucho(rank, P)
    else:
        comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    P    = comm.Get_size()

    FILAS = P-1
    COLS = FILAS * 2

    # RANK 0 crea la matriz y la envía al resto de procesos.
    if rank == 0:
        verifico = FILAS * COLS < maxMatrizElementos
        # 1. Distribuir filas por cada proceso (Cuidado con los tipos)
        matrix = np.random.rand(FILAS, COLS).astype(np.float32) # Ojo - era P en vez de FILAS
        if DEBUG:
            matrix.fill(1)

        if verifico:
            media_enviado = np.mean(matrix)
            print(f"DEBUG: Rank:{rank} media_enviado:{media_enviado}")
            print(f"INFO: Matriz:  {matrix}")
        else:
            print(f"WARN no verifico: FILAS * COLS ›= {maxMatrizElementos}")

        listaSumaFilas=list()
        # Envio:
        # ...
        for procesoFila in range(FILAS):
            data = matrix[procesoFila, :]
            comm.send(data, dest=procesoFila+1)

        # 2. Recibir resultados
        for procesoFila in range(FILAS):
            status = MPI.Status()
            data = comm.recv(source=MPI.ANY_SOURCE, status=status) #no-bloqueante
            print(f"DEBUG: Rank:{rank} recibo de {procesoFila}, data:{data}")
            #TODO: validar
            if status.Get_source() != 0:
                listaSumaFilas.append(data)


        media = sum(listaSumaFilas) / FILAS / COLS
        print("Resultado:", media)


    # RANKS 1 a P-1 reciben trabajo y envían resultados.
    else:
        # 1. Recibir datos
        status = MPI.Status()
        data = comm.recv(source=0, status=status) #bloqueante
        # TODO: validar
        result = np.sum(data)
        # 3. Enviar resultado.
        print(f"DEBUG: Rank:{rank} envío, data:{result}")
        comm.send(result, dest=0)
