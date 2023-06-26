import os

def almiento_segun_etapa(lista):
    print
    cosechas = [float(lista[1]), float(lista[2]), float(lista[3])]
    alimentos = []
    return cosechas


ruta = os.path.join("archivos", "archivos csv", "Base de Datos - Alpha_i,p.csv")
with open(ruta) as archivo:
    lista = archivo.readlines()[2:]

info_a_filtrar = []
for elementos in lista:
    limpio = elementos.strip().split(",")
    info_a_filtrar.append(limpio)


proteinas = almiento_segun_etapa(info_a_filtrar[0])
lipidos = almiento_segun_etapa(info_a_filtrar[1])
carbohidratos = almiento_segun_etapa(info_a_filtrar[2])
vitaminas = almiento_segun_etapa(info_a_filtrar[3])
alpha_iep = [proteinas,lipidos,carbohidratos,vitaminas]

if __name__ == "__main__":
    print(alpha_iep)

    

