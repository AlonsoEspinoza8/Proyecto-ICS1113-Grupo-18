import os
ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - CO_n,a.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()
#ponderador=1.3
ponderador=1
co_na = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    co_na.append([float(limpio[1])*ponderador,float(limpio[2])*ponderador,float(limpio[3])*ponderador])

if __name__ == "__main__":
    print(co_na)
