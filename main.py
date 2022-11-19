import pandas as pd
import os
import glob
import shutil

from collections import defaultdict
ruta_carpeta='C:/Users/lutay/Downloads/jobs/VALTX/CAJA'

def ruta_archivos(ruta=''):
    listado=os.listdir(ruta_carpeta+ruta)
    return listado
def cant_archivos(tipo_file,ruta=''):
    opcion=0
    if ruta=='':
        opcion=len(glob.glob(f"{ruta_carpeta}/*.{tipo_file}"))
    else:
        opcion = len(glob.glob(f"{ruta_carpeta}/{ruta}/*.{tipo_file}"))
    return opcion

clasificados = defaultdict(list)
directorios = []
for archivo in ruta_archivos():
    for elemento in os.scandir(f"{ruta_carpeta}/{archivo}"):
      nombre = elemento.name
      if elemento.is_dir():
        directorios.append(nombre)
      else:
        if "." in nombre:
          extension = nombre.split(".")[-1].lower()
        else:
          extension = ""
        clasificados[extension].append(nombre)

    bool_directorio=False
    bool_excel=False

    print("{} directorios".format(len(directorios)))
    for d in directorios:
        if (d=="CVL") | (d =="SVL"):
            bool_directorio=True
        else:
            bool_directorio = False


    print("{} ficheros".format(sum(len(caso) for caso in clasificados.values())))
    for k, v in clasificados.items():
        if (k=="xlsx") & (len(v)==1):
            bool_excel=True
        else:
            bool_excel=False


    # AQUI SOLO ENTRAN LAS CARPETAS QUE TIENEN UN ARCHIVO EXCEL Y >=1 CARPETA CON NOMBRE CVL O SVL
    if bool_excel & bool_directorio:
        print("APTO")
        #UNIFICANDO LAS IMG EN UNA SOLA CARPETA
        path_main = f"{ruta_carpeta}/{archivo}"
        list_files = os.listdir(path_main)
        os.mkdir(f"{path_main}/IMG_UNIFICADO")
        for file in list_files:
            if (file == "CVL") | (file == "SVL"):
                list_img = glob.glob(rf"{path_main}/{file}\*\*\*\*.tif")
                for img in list_img:
                    nombre_img = img.replace("\\", "/")
                    nombre_img = nombre_img.split("/")
                    nombre_img = nombre_img[-1]

                    path_origen = img.replace("\\", "/")
                    path_origen = path_origen.split("/")
                    path_origen.pop()
                    path_origen = '\\'.join(path_origen)
                    path_origen = path_origen.replace("\\", "/")

                    path_destino = f"{path_main}/IMG_UNIFICADO"

                    try:
                        src = os.path.join(path_origen, nombre_img)  # origen
                        dst = os.path.join(path_destino, nombre_img)  # destino
                        shutil.copy(src, dst)
                    except:
                        print("Error al unificar las imgs en el directorio")
                    else:
                        print("Cargado exitosamente")





    else:
        print("LA CARPETA NO CUMPLE CON LAS CARACTERISTICAS")



    directorios.clear()
    clasificados.clear()
    bool_directorio=False
    bool_excel=False
    print("--------------------------------")




