import os
ruta = os.path.join("archivos","archivos csv","Base de Datos - WP_p.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()


wp_p = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    wp_p=[float(limpio[1]),float(limpio[2]),float(limpio[3])]

if __name__ == "__main__":
    print(wp_p)
    