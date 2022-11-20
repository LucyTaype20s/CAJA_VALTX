import pandas as pd
import os
import glob
import shutil
import numpy as np
import datetime

from collections import defaultdict
ruta_carpeta='C:/Users/lutay/Downloads/jobs/VALTX/CAJA'
now = datetime.datetime.now()
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
        nombre_excel=''.join(v)

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
        #os.mkdir(f"{path_main}/IMG_UNIFICADO")
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

        # CREACIÓN EXCEL Y RENOMBRAMIENTO DE IMG
        print(f"{ruta_carpeta}/{archivo}/{nombre_excel}")
        df_indexacion = pd.read_excel(f"{ruta_carpeta}/{archivo}/{nombre_excel}", header=1)

        df_indexacion[df_indexacion["TIF"].str.contains(".tif")]
        conditions = [
            (df_indexacion['IDENTIFICADOR ÚNICO'].isna()) & (df_indexacion['NÚMERO DE DOCUMENTO'].isna()),
            (df_indexacion['IDENTIFICADOR ÚNICO'].isna()),
            (df_indexacion['IDENTIFICADOR ÚNICO'].notnull()),
        ]
        values = [
            df_indexacion['TELÉFONO / CELULAR'].astype(str) + "_" + str(
                now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif"),
            df_indexacion['NÚMERO DE DOCUMENTO'].astype(str) + "_" + str(
                now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif"),
            df_indexacion['IDENTIFICADOR ÚNICO'].astype(str) + "_" + str(
                now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif")
        ]
        df_indexacion['NOMBRE TIF'] = np.select(conditions, values)



        # -------------------------------------------------------------------

        ruta_carpeta_result="C:/Users/lutay/Downloads/jobs/VALTX/CAJA RESULTADO"

        os.mkdir(f"{ruta_carpeta_result}/{archivo}")
        os.mkdir(f"{ruta_carpeta_result}/{archivo}/IMG_")

        path_main = "C:/Users/lutay/Downloads/jobs/VALTX/CAJA/"
        list_imgs = os.listdir(f"{path_main}/{archivo}/IMG_UNIFICADO")
        df_imgs = pd.DataFrame(list_imgs, columns=['TIF'])
        df_imgs["EXISTENTE"] = "SI"

        df_homologado = df_indexacion.merge(df_imgs, how='left', on='TIF')
        df_homologado = df_homologado[df_homologado["EXISTENTE"] == "SI"]
        df_homologado.to_csv(f"{ruta_carpeta_result}/{archivo}/ReporteIndexacion.csv",
                             encoding='utf8')

        df_homologado2 = df_homologado[["TIF", "NOMBRE TIF"]]
        df_homologado2 = df_homologado2.to_numpy().tolist()
        # -------------------------------------------------------------------

        df_homologado = df_homologado["TIF"]
        df_homologado = df_homologado.to_numpy().tolist()

        for i in list_imgs:
            if i in df_homologado:
                path_main = "C:/Users/lutay/Downloads/jobs/VALTX"
                path_origen = f"{path_main}/CAJA/{archivo}/IMG_UNIFICADO"
                path_destino = f"{ruta_carpeta_result}/{archivo}/IMG_"
                print(df_homologado2[df_homologado.index(i)][1])
                try:

                    src = os.path.join(path_origen, i)  # origen
                    dst = os.path.join(path_destino, df_homologado2[df_homologado.index(i)][1])  # destino
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




