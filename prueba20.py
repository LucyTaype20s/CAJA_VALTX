import os
import shutil
import glob

path_main="C:/Users/lutay/Downloads/jobs/VALTX/CAJA/301061642_RONNY CERRADO"
list_files=os.listdir(path_main)
os.mkdir(f"{path_main}/IMG_UNIFICADO")
for file in list_files:
    if (file=="CVL") | (file=="SVL"):
        list_img=glob.glob(rf"{path_main}/{file}\*\*\*\*.tif")
        for img in list_img:
            nombre_img=img.replace("\\","/")
            nombre_img=nombre_img.split("/")
            nombre_img=nombre_img[-1]

            path_origen = img.replace("\\","/")
            path_origen=path_origen.split("/")
            path_origen.pop()
            path_origen='\\'.join(path_origen)
            path_origen=path_origen.replace("\\","/")

            path_destino=f"{path_main}/IMG_UNIFICADO"

            try:
                src = os.path.join(path_origen, nombre_img)  # origen
                dst = os.path.join(path_destino, nombre_img)  # destino
                shutil.copy(src, dst)
            except:
                print("Error al unificar las imgs en el directorio")
            else:
                print("Cargado exitosamente")
