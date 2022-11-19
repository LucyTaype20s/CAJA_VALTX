import pandas as pd
import os
import openpyxl
#ruta_carpeta='C:/Users/lutay/Downloads/jobs/VALTX/CAJA'

#df=pd.read_excel(f"{ruta_carpeta}/301032774_RONNY CERRADO/0301032774.xlsx")

#new=df.loc[1:5]
#print(new)
path_main="C:/Users/lutay/Downloads/jobs/VALTX/CAJA/301061642_RONNY CERRADO"
list_imgs=os.listdir(f"{path_main}/IMG_UNIFICADO")
list_imgs.insert(0,"TIF")
print(list_imgs)