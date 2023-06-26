import os
#ponderador = 20
ponderador =   1
ruta = os.path.join("archivos", "archivos csv", "Base de Datos - d_p,t.csv")
with open(ruta) as archivo:
    d_prt = []
    lista = archivo.readlines()[1:]
    for elementos in lista:
        limpio = elementos.strip().split(",")
        r=[int(limpio[1]) * ponderador,int(limpio[2]) * ponderador,int(limpio[3]) * ponderador]
        d_prt.append(r)

if __name__ == "__main__":
    print(d_prt)