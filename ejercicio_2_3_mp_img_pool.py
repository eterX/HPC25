import multiprocessing as mp
import numpy as np
import time
import sys
import os
import cv2

# Config
folder_in  = "data/image_set"
folder_out = "data/image_set/output"


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

    nombre = mp.current_process().name
    print("Proceso", nombre, "procesando:", imagen_in, " ==>> ", imagen_out)

    img = cv2.imread(imagen_in)

    res = procesar_cv(img)

    cv2.imwrite(imagen_out, res)
    # time.sleep(0.1)


if __name__ == '__main__':

    start = time.time()

    # 1. Establecer ruta:
    os.makedirs(folder_out, exist_ok = True)



    #secuencial
    if False:
        for imagen in os.listdir(folder_in):
            if (imagen.endswith(".png") or imagen.endswith(".jpg") or imagen.endswith(".jpeg")):
                # 2. Procesar
                procesar_imagen(imagen) # No necesito la salida
    for imagen in os.listdir(folder_in):
        if (imagen.endswith(".png") or imagen.endswith(".jpg") or imagen.endswith(".jpeg")):
            # 2. Procesar
            procesar_imagen(imagen) # No necesito la salida



    end = time.time()
    print("Time:", end - start)
