import glob
import os
from collections import Counter
import pandas as pd
import datetime
import shutil
import numpy as np

now = datetime.datetime.now()
indice=0

def replace_ (string):
    string=string.replace("\\","/")
    return string


path_main="C:/Users/lutay/Downloads/jobs/VALTX"

list_iCaja=[]
list_img=[]
cant_excel=[]
list_nombre_img=[]
list_ruta_img=[]
"""
count=0
for caja in os.scandir(f"{path_main}/CAJA"):
    cant_excel=glob.glob(f"{path_main}/CAJA/{caja.name}/*.xlsx")
    list_iCaja=os.listdir(f"{path_main}/CAJA/{caja.name}")
    count=Counter(list_iCaja)
    if (os.path.isdir(f"{path_main}/CAJA RESULTADO/{caja.name}")):
        shutil.rmtree(f"{path_main}/CAJA RESULTADO/{caja.name}")
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




                os.mkdir(f"{path_main}/CAJA RESULTADO/{caja.name}")
                os.mkdir(f"{path_main}/CAJA RESULTADO/{caja.name}/img")

                #-------------------------------------------------------------------------

                df_excel = pd.read_excel(f"{path_main}/CAJA/{caja.name}/{i_caja.name}", header=1)
                df_excel["TIF"].fillna("-", inplace=True)
                df_excel = df_excel[df_excel["TIF"].str.contains(".tif")]
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
                df_homologado = df_homologado[df_homologado["EXISTENTE"] == "SI"]

                lista_lucy=pd.DataFrame(list_nombre_img)
                lista_lucy.to_csv(f"{path_main}/CAJA RESULTADO/{caja.name}/ListadoTIF.csv", encoding='utf-8')
                df_homologado.to_csv(f"{path_main}/CAJA RESULTADO/{caja.name}/IndexacionMATH.csv", encoding='utf-8')
                df_homologado2 = df_homologado[["TIF", "NOMBRE TIF"]]
                df_homologado2 = df_homologado2.to_numpy().tolist()

                df_homologado = df_homologado["TIF"]
                df_homologado = df_homologado.to_numpy().tolist()
                print("CANTIDAD DE FILAS ES LA LISTA DE IMAGENES:  ---->  " + str(len(list_nombre_img)))

                for i in list_nombre_img:
                    indice = indice + 1
                    if i in df_homologado:
                        path_origen = f"{list_ruta_img[indice - 1]}"
                        path_destino = f"{path_main}/CAJA RESULTADO/{caja.name}/img"
                        try:
                            src = os.path.join(path_origen, i)  # origen
                            dst = os.path.join(path_destino, df_homologado2[df_homologado.index(i)][1])  # destino
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
    print("------------------------------------")"""

lista_nueva=os.listdir(f"{path_main}/CAJA RESULTADO")
for i in lista_nueva:
    for j in os.listdir(f"{path_main}/CAJA RESULTADO/{i}"):

        """cant_img=glob.glob(f"{path_main}/CAJA RESULTADO/{i}/*/*.tif")
        #print(cant_img)
        df_homologado=pd.DataFrame(cant_img)
        df_homologado.to_csv(f"{path_main}/CAJA RESULTADO/{i}/ListadoIMGTIF.csv", encoding='utf-8')
        print(f"LA CAJA {i} : "+str(len(cant_img)))"""
        if os.path.exists(f"{path_main}/CAJA/{i}/ReporteIndexación.xlsx"):
            os.remove(f"{path_main}/CAJA/{i}/ReporteIndexación.xlsx")
    print("----------------------------")


