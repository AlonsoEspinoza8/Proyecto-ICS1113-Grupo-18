import os
# s, e , p
#ponderador = 1.3
ponderador=1
ruta = os.path.join("archivos", "archivos csv", "Base de Datos - PE_s,p.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()
    info_a_filtrar = []
    for elementos in lista[2:]:
        limpio = elementos.strip().split(",")
        info = [[int(limpio[1]) * ponderador,int(limpio[2]) * ponderador,int(limpio[3]) * ponderador],
                [int(limpio[4]) * ponderador,int(limpio[5]) * ponderador ,int(limpio[6]) * ponderador],
                [int(limpio[7]) * ponderador,int(limpio[8]) * ponderador,int(limpio[9]) * ponderador]]
        
PE_sep=info

    # LISTO