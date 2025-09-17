from mpi4py import MPI
import numpy as np
import time

if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    P    = comm.Get_size()

    FILAS = P
    COLS =  FILAS*1

    # RANK 0 crea la matriz y la envía al resto de procesos.
    if rank == 0:

        # 1. Distribuir filas por cada proceso (Cuidado con los tipos)
        matrix = np.random.rand(FILAS, COLS).astype(np.float32) # Ojo - era P
        media_enviado = np.mean(matrix)
        print("Matriz: \n", matrix)
        print(f"DEBUG: Rank:{rank} media_enviado:{media_enviado}")
        listaMediaFilas=list()
        # Envio:
        # ...
        for procesoFila in range(FILAS):
            data = matrix[procesoFila, :]
            comm.send(data, dest=procesoFila)

        # 2. Recibir resultados
        for procesoFila in range(FILAS):
            data = comm.recv(source=MPI.ANY_SOURCE)
            print(f"DEBUG: Rank:{rank} recibo de {procesoFila}, data:{data}")
            #TODO: validar
            listaMediaFilas.append(data)


        media = sum(listaMediaFilas) / len(listaMediaFilas)
        print("Resultado:", media)


    # RANKS 1 a P-1 reciben trabajo y envían resultados.
    else:
        # 1. Recibir datos
        data = comm.recv(source=0)

        # 2. Realizar cómputo
        result = np.mean(data)

        # 3. Enviar resultado.
        comm.send(result, dest=0)
