import os

ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - V[s,t,p].csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

peces_ingreso = []

for elementos in lista[2:]:
    limpio = elementos.strip().split(",")

    s1 = ([float(limpio[1]), float(limpio[2]), float(limpio[3])])
    s2 = [float(limpio[4]), float(limpio[5]), float(limpio[6])]
    s3 = ([float(limpio[6]), float(limpio[7]), float(limpio[8])])

    peces_ingreso.append([s1, s2, s3])

if __name__ == "__main__":
    print(peces_ingreso)