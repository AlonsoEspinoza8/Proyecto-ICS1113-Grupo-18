import os
#s, t
ruta = os.path.join("archivos", "archivos csv", "Base de Datos - TOP_n,s,t.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()

info_a_filtrar = []
for elementos in lista[2:]:
    limpio = elementos.strip().split(",")
    limpio=limpio[1:7]
    sal1=[int(limpio[0]),int(limpio[1])]
    sal2=[int(limpio[2]),int(limpio[3])]
    sal3=[int(limpio[4]),int(limpio[5])]
    info_a_filtrar.append([sal1,sal2,sal3]) 
tope_st =info_a_filtrar
#print(tope_st)
#if __name__ == "__main__":
    #print(f"Topes de la salmonera 1: {tope_st[0]}")
    #print(f"Topes de la salmonera 1 en el año 5: {tope_st[0][5]}")
    # LISTO
