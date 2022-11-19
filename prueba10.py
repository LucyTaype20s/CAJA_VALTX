import os
import shutil
import glob

directorio_main=f"C:/Users/lutay/Downloads/jobs/VALTX/CAJA/301061642_RONNY CERRADO"


list_download=os.listdir(directorio_main)
#os.mkdir(f"{directorio_main}/IMG_UNIFICADO2")


for item in list_download:
    nuevo=item.replace("/",r"--\--")
    nuevo=nuevo.replace("--","")
    print(nuevo)

    if (item=="CVL") | (item=="SVL"):

        lista_glob = glob.glob(rf"{directorio_main}/{item}\*\*\*\*.tif")
        for elemento in lista_glob:
            nuevo = elemento.replace("/", r"--\--")
            nuevo = nuevo.replace("--", "")
            #print(nuevo)

            #pathCarpeta=glob.glob(rf"{directorio_main}/{elemento}\*\*")

            destino=rf"{directorio_main}\IMG_UNIFICADO2"
            destino=destino.replace("/", r"--\--")
            destino=destino.replace("--", "")
            pathCarpeta=nuevo.split("\\")
            pathCarpeta.pop()
            pathCarpeta='\\'.join(pathCarpeta)
            pathCarpeta2 = destino

            pathCarpeta=pathCarpeta.replace("\\","/")
            pathCarpeta2=pathCarpeta2.replace("\\","/")
            nuevo=nuevo.replace("\\","/")
            print("ORIGEN:  " + pathCarpeta)
            print("DESTINO:  " + pathCarpeta2)

            nuevo=nuevo.split("/")
            nuevo=nuevo[-1]

            try:

                print(f"Copiando {nuevo} --> {pathCarpeta2} ... ", end="")
                src = os.path.join(pathCarpeta, nuevo) # origen

                dst = os.path.join(f"{pathCarpeta2}", nuevo) # destino
                shutil.copy(src, dst)
                print("Correcto")
            except:
                print("Falló")
                print("Error, no se pudo copiar el archivo. Verifique los permisos de escritura")

