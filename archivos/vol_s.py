import os
ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - VOL_s.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

vol = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    vol.append(int(limpio[1]))

if __name__ == "__main__":
    print(vol)
