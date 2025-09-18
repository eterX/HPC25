from mpi4py import MPI
import numpy as np
import time
import sys
import os
import cv2

# Config
folder_in  = "../data/image_set"
folder_out = "../data/image_set/output"


def procesar_cv(img):

    (alto, ancho, canales) = img.shape

    alto  = 1024
    ancho = 1024

    res = cv2.resize(img, (int(ancho), int(alto)), interpolation = cv2.INTER_AREA)

    kernel=(11,11)
    gaussian = cv2.GaussianBlur(res, kernel, 0)

    M = cv2.getRotationMatrix2D((ancho, alto), 45, 1) # grados y dirección (clockwise)
    rot = cv2.warpAffine(gaussian, M, (ancho, alto))

    M = np.float32([[1, 0, 100], [0, 1, -100]])
    tras = cv2.warpAffine(rot, M, (ancho, alto))

    gris_img = cv2.cvtColor(tras, cv2.COLOR_BGR2GRAY)
    thrs_img = cv2.adaptiveThreshold(gris_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return thrs_img


def procesar_imagen (imagen):

    imagen_in  = folder_in + "/" + imagen
    imagen_out = folder_out + "/" + imagen

    img = cv2.imread(imagen_in)

    res = procesar_cv(img)

    cv2.imwrite(imagen_out, res)


if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    P    = comm.Get_size()

    if rank == 0:                     # Root lee nombres de archivos a procesar
        start = time.time()

        # 1. Establecer ruta:
        os.makedirs(folder_out, exist_ok = True)
        nombres_imgs = list()

        for imagen in os.listdir(folder_in):
            if (imagen.endswith(".png") or imagen.endswith(".jpg") or imagen.endswith(".jpeg")):
                nombres_imgs.append(imagen)

        n_imgs = np.array(nombres_imgs).reshape(P, -1)  # Uso de scatter

    else:
        n_imgs = None

    # 2. Distribuir los nombres
    recv_lista = comm.scatter(n_imgs, root=0)              # Distribuir lista de nombres

    for nombre in recv_lista:
        procesar_imagen(nombre)                         # Cada P su parte

    if rank == 0:
        end = time.time()
        print("Time:", end - start)
