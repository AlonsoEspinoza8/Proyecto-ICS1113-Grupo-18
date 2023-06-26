import os


ruta = os.path.join("archivos", "archivos csv", "Base de Datos - Epsilon_i,a.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()
#ponderador=1.2
ponderador=1
epsilon_ia = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    epsilon_ia.append([float(limpio[1])*ponderador, float(limpio[2])*ponderador, float(limpio[3])*ponderador])

if __name__ == "__main__":
    print(epsilon_ia)