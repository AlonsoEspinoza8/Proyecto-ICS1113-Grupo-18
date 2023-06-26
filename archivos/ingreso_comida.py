import os

ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - Ingreso_alimento.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

alimentos_ingreso = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    alimentos_ingreso.append(int(limpio[1]))

if __name__ == "__main__":
    print(alimentos_ingreso)