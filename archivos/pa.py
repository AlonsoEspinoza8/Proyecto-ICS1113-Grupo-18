import os
ruta = os.path.join( "archivos", "archivos csv", "Base de Datos - PA_s,a.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

pa_sa = []
for elementos in lista[1:]:
    limpio = elementos.strip().split(",")
    r = [float(limpio[1]),float(limpio[2]),float(limpio[3])]
    pa_sa.append(r)

if __name__ == "__main__":
    print(pa_sa)
