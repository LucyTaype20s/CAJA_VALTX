import glob
import os
from collections import Counter
import pandas as pd
import datetime
import shutil
import numpy as np

from datetime import datetime

def replace_ (string):
    string=string.replace("\\","/")
    return string

path_main="C:/Users/lutay/Downloads/jobs/VALTX"


list_img=[]
list_img_x_VL=[]
list_nombre_img_x_VL=[]
list_ruta_img_x_VL=[]

list_info_img=[]
now = datetime.now()


list_cajas=os.scandir(f"{path_main}/CAJA")

for caja in list_cajas:
    if os.path.exists(f"{path_main}/CAJA/{caja.name}/ReporteIndexación.xlsx"):
        os.remove(f"{path_main}/CAJA/{caja.name}/ReporteIndexación.xlsx")
    if os.path.exists(f"{path_main}/CAJA/{caja.name}/ListaHomologada.xlsx"):
        os.remove(f"{path_main}/CAJA/{caja.name}/ListaHomologada.xlsx")

    cant_excel = glob.glob(f"{path_main}/CAJA/{caja.name}/*.xlsx")
    list_iCaja = os.listdir(f"{path_main}/CAJA/{caja.name}")
    count = Counter(list_iCaja)
    if (os.path.isdir(f"{path_main}/CAJA/{caja.name}/img")):
        shutil.rmtree(f"{path_main}/CAJA/{caja.name}/img")
    if ((count["CVL"] == 1) | (count["SVL"] == 1)) & (len(cant_excel) == 1):
        list_excelResumen=glob.glob(f"{path_main}/CAJA/{caja.name}/*/*xls")
        print("CAJA: "+caja.name)

        # EN ESTE FOR LA CANTIDAD DE RECORRIDOS ES MAX 2 POR LAS CARPETAS SVL / CVL
        for excel_resumen in list_excelResumen:

            df_resumen=pd.read_excel(replace_(excel_resumen),header=1)
            #df_resumen['FECHA'] = pd.to_datetime(df_resumen['FECHA'], format='%Y%m%d',errors='coerce')
            tipo_VL=replace_(excel_resumen).split("/")
            df_resumen["TIPO_VL"]=tipo_VL[-2]




            #df_resumen['FECHA']=df_resumen['FECHA'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df_resumen["COD TIF"]=df_resumen['TITULO'].str.cat(df_resumen['TIPO_VL'],sep="-")

            
            

            
            list_img=glob.glob(f"{path_main}/CAJA/{caja.name}/*/*/*/*/*.tif")

            ruta_hastaVL=replace_(excel_resumen).split("/")
            ruta_hastaVL.pop()
            ruta_hastaVL='/'.join(ruta_hastaVL)

            list_img_x_VL=glob.glob(f"{ruta_hastaVL}/*/*/*/*.tif")
            for img in list_img_x_VL:
                list_ruta_img=img
                list_ruta_img=replace_(list_ruta_img).split("/")
                list_ruta_img.pop()
                ruta_img='/'.join(list_ruta_img)
                list_ruta_img_x_VL.append(ruta_img)
                #------------------------
                list_nombre_img=replace_(img).split("/")
                list_nombre_img=list_nombre_img[-1]
                nombre_img_x_VL=''.join(list_nombre_img)
                list_nombre_img_x_VL.append(nombre_img_x_VL)
            #ESTAMOS EN LA SGT RUTA --> ./*/*/N/RESUMEN_EXCEL . OBTUVIMOS EL LISTADO DE LOS NOMBRES DE LAS IMG SEPARADO POR LISTAS, UNA LISTA X CADA TIPO DE VALOR LEGAL
            list_img_nombreYruta=list(zip(list_nombre_img_x_VL,list_ruta_img_x_VL))
            df_img_x_VL=pd.DataFrame(list_img_nombreYruta,columns=["TITULO","RUTA"])
            df_img_x_VL["EXISTENTE"]="SI"
            df_resumen_main=df_resumen.merge(df_img_x_VL, how='left', on='TITULO')
            df_resumen_main=df_resumen_main[df_resumen_main["EXISTENTE"] == "SI"]

            # ESTRUCTURA DE LA LISTA QUE CONTIENE TODAS LAS IMAGENES DE LA CAJA ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            df_resumen_main=df_resumen_main[["TITULO","COD TIF","RUTA"]]

            df_list_resumen_main = df_resumen_main.to_numpy().tolist()

            for row in df_list_resumen_main:
                list_info_img.append(row)

            list_nombre_img_x_VL.clear()
            list_ruta_img_x_VL.clear()
            
        print("CANTIDAD DE IMAGENES EN LA CAJA: "+str(len(list_info_img)))
        

        #---------------------------------------------------------------------------------------------

        for i_caja in os.scandir(f"{path_main}/CAJA/{caja.name}"):
            if i_caja.is_dir()==False:

                os.mkdir(f"{path_main}/CAJA/{caja.name}/img")

                #-------------------------------------------------------------------------------------
                df_excel = pd.read_excel(f"{path_main}/CAJA/{caja.name}/{i_caja.name}", header=1)
                print("NOMBRE EXCEL: "+i_caja.name)

                df_excel["TIPO"].fillna("-", inplace=True)

                conditions_tipo = [
                    (df_excel['TIPO']=="AZURE"),
                    (df_excel['TIPO']=="SVL"),
                    (df_excel['TIPO']=="CVL"),
                ]
                values_tipo = [
                    "SVL",
                    "SVL",
                    "CVL"
                ]
                df_excel['TIPO_VL'] = np.select(conditions_tipo, values_tipo)
                df_excel['COD TIF']=df_excel['TIF'].str.cat(df_excel['TIPO_VL'],sep="-")

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

                #CREANDO LA COLUMNA QUE SERÁ EL ID EN EL MERGE CON EL LISTADO DE IMGS

                df_list_img=pd.DataFrame(list_info_img,columns=["TIF RESUMEN",'COD TIF',"RUTA"])
                df_list_img["EXISTENTE"]="SI"

                df_homologado = df_excel.merge(df_list_img, how='left', on='COD TIF')
                df_homologado["EXISTENTE"].fillna("NO", inplace=True)
                df_homologado["FECHA EJECUCION"] = now.strftime("%Y-%m-%d %H:%M:%S")

                df_homologado.to_excel(f"{path_main}/CAJA/{caja.name}/ReporteIndexación.xlsx", index=False)

                df_existente = df_homologado[df_homologado["EXISTENTE"] == "SI"]



                #print(df_existente["NOMBRE TIF"])
                df_existente = df_existente[["TIF", "NOMBRE TIF","COD TIF"]]

                df_listInfoTif_listado=pd.DataFrame(list_info_img,columns=["TITULO","COD TIF","RUTA"])
                df_listInfoTif_Indexacion=pd.DataFrame(df_existente,columns=["TIF", "NOMBRE TIF","COD TIF"])
                df_listInfoTif_Unificado=df_listInfoTif_listado.merge(df_listInfoTif_Indexacion, how='left', on='COD TIF')

                df_listInfoTif_Unificado.to_excel(f"{path_main}/CAJA/{caja.name}/ListaHomologada.xlsx", index=False)


                df_existenteCODTif = df_existente["COD TIF"]
                df_existenteNOMBRETif=df_existente["NOMBRE TIF"]

                df_existente = df_existente.to_numpy().tolist()
                df_existenteCODTif = df_existenteCODTif.to_numpy().tolist()
                df_existenteNOMBRETif=df_existenteNOMBRETif.to_numpy().tolist()

                df_listCODIGOIMG=df_listInfoTif_Unificado["NOMBRE TIF"]
                df_listInfoTif_Unificado=df_listInfoTif_Unificado.to_numpy().tolist()
                df_listCODIGOIMG=df_listCODIGOIMG.to_numpy().tolist()


                for i in df_listInfoTif_Unificado:
                    try:
                        path_origen=f"{i[2]}"
                        name_img_origen=f"{i[0]}"

                        #ORIGEN
                        src=f"{path_origen}/{name_img_origen}"

                        name_img_destino=f"{i[4]}"

                        #DESTINO

                        dst=f"{path_main}/CAJA/{caja.name}/img/{name_img_destino}"

                        shutil.copy(src, dst)
                    except:
                        print("Error al unificar las imgs en el directorio")
                    print("----")







            else:
                "ESTA ES UNA CARPETA"


    list_info_img.clear()

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

list_img_unificado=os.listdir(f"{path_main}/CAJA")
for i in list_nombre_img:
    print(i)
print("-----------------------")

