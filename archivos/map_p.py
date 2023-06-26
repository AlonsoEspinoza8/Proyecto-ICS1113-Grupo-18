import os

ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - MAP_p.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

map = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    map.append(int(limpio[1]))

if __name__ == "__main__":
    print(map)