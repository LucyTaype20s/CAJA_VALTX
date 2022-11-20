import glob
import os
import pandas as pd
import openpyxl
import datetime
import numpy as np
import shutil

now = datetime.datetime.now()
def replace_ (string):
    string=string.replace("\\","/")
    return string

path_main="C:/Users/lutay/Downloads/jobs/VALTX"
n_carpetas1=[]
n_archivos1=[]
list_imagenesTIF=[]
list_imagenesTIF_copy=[]

list_cajas=os.scandir(f"{path_main}/CAJA")

for caja in list_cajas:
    item_caja=os.scandir(f"{path_main}/CAJA/{caja.name}")
    for i in item_caja:
        nombre_elemento=i.name
        if (i.is_dir()) & ((nombre_elemento=='SVL')|(nombre_elemento=='CVL')):
            n_carpetas1.append(nombre_elemento)
        if ".xlsx" in nombre_elemento:
            n_archivos1.append(nombre_elemento)
    if (len(n_carpetas1)>=1) & (len(n_archivos1)==1):












        for i_caja in os.scandir(f"{path_main}/CAJA/{caja.name}"):
            list_img=glob.glob(f"{path_main}/CAJA/{caja.name}/*/*/*/*/*.tif")
            for img in list_img:
                path_img=replace_(img).split("/")
                nombre_img=img
                path_img.pop()
                path_img='/'.join(path_img)
                nombre_img=replace_(nombre_img).split("/")
                nombre_img=nombre_img[-1]
                nombre_img=''.join(nombre_img)
                list_imagenesTIF.append(nombre_img)
            print(list_imagenesTIF)
            """
            if i_caja.name.__contains__(".xlsx"):
                df_excel=pd.read_excel(f"{path_main}/CAJA/{caja.name}/{i_caja.name}",header=1)
                df_excel["TIF"].fillna("-",inplace=True)
                df_excel=df_excel[df_excel["TIF"].str.contains(".tif")]
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

                if (os.path.isdir(f"{path_main}/CAJA RESULTADO/{caja.name}"))| (os.path.isdir(f"{path_main}/CAJA RESULTADO/{caja.name}/img")) :
                    shutil.rmtree(f"{path_main}/CAJA RESULTADO/{caja.name}")
                    print("ENTRÓ AL IFFF")

                else:
                    print("ENTRÓ AL ELSE")
                os.mkdir(f"{path_main}/CAJA RESULTADO/{caja.name}")
                os.mkdir(f"{path_main}/CAJA RESULTADO/{caja.name}/img")

                df_list_img=pd.DataFrame(list_imagenesTIF_copy,columns=["TIF"])
                df_list_img["EXISTENTE"]="SI"
                #print(list_imagenesTIF_copy)
                df_homologado=df_excel.merge(df_list_img,how='left',on='TIF')
                df_homologado=df_homologado[df_homologado["EXISTENTE"]=="SI"]
                df_homologado.to_csv(f"{path_main}/CAJA RESULTADO/{caja.name}/IndexacionMATH.csv",encoding='utf-8')
                df_homologado2 = df_homologado[["TIF", "NOMBRE TIF"]]
                df_homologado2 = df_homologado2.to_numpy().tolist()

                    # -------------------------------------------------------------------

                df_homologado = df_homologado["TIF"]
                df_homologado = df_homologado.to_numpy().tolist()
                print("CANTIDAD DE FILAS ES LA LISTA DE IMAGENES:  ---->  "+str(len(list_imagenesTIF_copy)))
                for i in list_imagenesTIF_copy:
                    path_origen=f"{path_img}"
                    path_destino=f"{path_main}/CAJA RESULTADO/{caja}/img"
                    try:
                        src = os.path.join(path_origen, i)  # origen
                        dst = os.path.join(path_destino, df_homologado2[df_homologado.index(i)][1])  # destino
                        shutil.copy(src, dst)
                    except:
                        print("Error al unificar las imgs en el directorio")
                    else:
                        print("Cargado exitosamente")"""
















        list_imagenesTIF.clear()
        list_imagenesTIF_copy.clear()


























    else:
        print("NO APTO")
    print("------------------------------------------------------------------------------------------------")

    n_carpetas1.clear()
    n_archivos1.clear()