import os
# n, a

ruta = os.path.join("archivos", "archivos csv", "Base de Datos - Beta_n,a.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()


beta_na = []
ponderador=0
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    beta_na.append([float(limpio[1]), float(limpio[2]), float(limpio[3])])

if __name__ == "__main__":
    print(beta_na)

    
