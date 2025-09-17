import multiprocessing as mp
import time

def fxn(conn):
    msg = conn.recv()
    print(msg)

    print(conn.recv())
    conn.close()

if __name__ == '__main__':

    p_conn, h_conn = mp.Pipe()
    p = mp.Process(target=fxn, args=(h_conn,))
    p.start()

    p_conn.send(["Hola", 0])
    p_conn.send(["Adiós", 1])
    p_conn.close()

    p.join()
