import glob
import os
from collections import Counter
import pandas as pd
import datetime
import shutil
import numpy as np

def replace_ (string):
    string=string.replace("\\","/")
    return string

path_main="C:/Users/lutay/Downloads/jobs/VALTX"
now = datetime.datetime.now()

indice=0

list_iCaja=[]
list_img=[]
cant_excel=[]
list_nombre_img=[]
list_ruta_img=[]

count=0
for caja in os.scandir(f"{path_main}/CAJA"):
    cant_excel=glob.glob(f"{path_main}/CAJA/{caja.name}/*.xlsx")
    list_iCaja=os.listdir(f"{path_main}/CAJA/{caja.name}")
    count=Counter(list_iCaja)
    if (os.path.isdir(f"{path_main}/CAJA/{caja.name}/img")):
        shutil.rmtree(f"{path_main}/CAJA/{caja.name}/img")
    if ((count["CVL"]==1) | (count["SVL"]==1))&(len(cant_excel)==1):

        for i_caja in os.scandir(f"{path_main}/CAJA/{caja.name}"):

            if i_caja.is_dir()==False:
                list_img=glob.glob(f"{path_main}/CAJA/{caja.name}/*/*/*/*/*.tif")
                for tif in list_img:
                    list_img=replace_(tif).split("/")
                    nombre_img = list_img[-1]
                    list_img.pop()
                    ruta_img='/'.join(list_img)
                    list_nombre_img.append(nombre_img)
                    list_ruta_img.append(ruta_img)
                print(len(list_nombre_img))
                print(len(list_ruta_img))

                # CREACION CARPETA IMG
                os.mkdir(f"{path_main}/CAJA/{caja.name}/img")

                df_excel = pd.read_excel(f"{path_main}/CAJA/{caja.name}/{i_caja.name}", header=1)
                df_excel["TIF"].fillna("-", inplace=True)
                conditions = [
                    (df_excel['IDENTIFICADOR ÚNICO'].isna()) & (df_excel['NÚMERO DE DOCUMENTO'].isna()),
                    (df_excel['IDENTIFICADOR ÚNICO'].isna()),
                    (df_excel['IDENTIFICADOR ÚNICO'].notnull()),
                ]
                values = [
                    df_excel['TELÉFONO / CELULAR'].astype(str) + "_" + str(
                        now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif"),
                    df_excel['NÚMERO DE DOCUMENTO'].astype(str) + "_" + str(
                        now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif"),
                    df_excel['IDENTIFICADOR ÚNICO'].astype(str) + "_" + str(
                        now.strftime("%d%m%Y") + "_" + str(now.strftime("%H%M%S")) + ".tif")
                ]
                df_excel['NOMBRE TIF'] = np.select(conditions, values)

                df_list_img = pd.DataFrame(list_nombre_img, columns=["TIF"])
                df_list_img["EXISTENTE"] = "SI"

                df_homologado = df_excel.merge(df_list_img, how='left', on='TIF')

                df_homologado["EXISTENTE"].fillna("NO", inplace=True)
                df_homologado["FECHA EJECUCION"]=now.strftime("%Y-%m-%d %H:%M:%S")

                df_homologado.to_excel(f"{path_main}/CAJA/{caja.name}/ReporteIndexación.xlsx",index=False)

                df_existente=df_homologado[df_homologado["EXISTENTE"]=="SI"]
                df_existente=df_existente[["TIF","NOMBRE TIF"]]
                df_existenteNombreTif=df_existente["TIF"]

                df_existente=df_existente.to_numpy().tolist()
                df_existenteNombreTif=df_existenteNombreTif.to_numpy().tolist()





                for i in list_nombre_img:
                    indice = indice + 1
                    if i in df_existenteNombreTif:
                        path_origen = f"{list_ruta_img[indice - 1]}"
                        path_destino = f"{path_main}/CAJA/{caja.name}/img"
                        try:
                            src = os.path.join(path_origen, i)
                            dst = os.path.join(path_destino, df_existente[df_existenteNombreTif.index(i)][1])
                            shutil.copy(src, dst)
                        except:
                            print("Error al unificar las imgs en el directorio")

                indice = 0

                list_ruta_img.clear()
                list_nombre_img.clear()
                list_img.clear()

            else:
                print("CARPETA")
    else:
        print("NO APTO")
    print("------------------------------------")