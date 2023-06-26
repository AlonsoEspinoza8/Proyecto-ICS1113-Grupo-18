import os
ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - PC_p.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

pc_p = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    pc_p.append([float(limpio[1]),float(limpio[2]),float(limpio[3])])

if __name__ == "__main__":
    print(pc_p)
