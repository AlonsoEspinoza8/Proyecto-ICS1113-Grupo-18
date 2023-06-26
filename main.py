from gurobipy import GRB, Model
from gurobipy import quicksum
from random import randint, seed, random
# import matplotlib.pyplot as plt # Si se tiene descargada se pueden ver los gráficos comentados en la parte inferior del código

# Importar parámetros
from archivos.alpha import alpha_iep
from archivos.beta import beta_na
from archivos.map_p import map
from archivos.epsilon import epsilon_ia
from archivos.demanda import d_prt
from archivos.peces_iniciales import PE_sep
from archivos.tope import tope_st
from archivos.vol_s import vol
from archivos.pa import pa_sa
from archivos.co import co_na
from archivos.pc import pc_p
from archivos.wp_p import wp_p
from archivos.ingreso import peces_ingreso
from archivos.ingreso_comida import alimentos_ingreso

seed(10)
# 1) Generar el modelo
model = Model()
model.setParam("TimeLimit", 1800)

# 2) Generar los conjuntos

P_ = range(3) #tipo de peces
T_ = range(25) #horizonte temporal
S_ = range(3) #salmoneras
N_ = range(2) #externalidades negativas
A_ = range(3) #marca del alimento
I_ = range(4) #nutrientes

# --------------------- Importar parámetros creados  ------------------#
Big_M = 10**100
alpha = {(i,p): alpha_iep[i][p] for i in I_ for p in P_} #mínimo requerido de cada nuetriente por cada pez
beta = {(n,p): beta_na[n][p] for n in N_ for p in P_ } #cantidad de contaminante orgánico que genera el alimento 
d = {(t,p): d_prt[t][p] for p in P_  for t in T_} #demanda 
WP = {(p): wp_p[p] for p in P_ } #peso de cada pez
PE = {(s,p): PE_sep[s][p] for s in S_ for p in P_} #cantidad inicial de peces
MAP={(p): map[p] for p in P_} #densidad maxima 
VOL={(s): vol[s]for s in S_} #volumen de salmonera
epsilon = {(i,a): epsilon_ia[i][a] for i in I_ for a in A_} #porcentaje de cada nuetriente que tiene cada alimento
TOP = {(t,s,n): tope_st[t][s][n] for s in S_  for t in T_ for n in N_} #tope permitido de exteranlidades por cada salmonera
PA = {(a,s): pa_sa[a][s] for s in S_ for a in A_} #cantidad inicial de alimento
CO={(n,a): co_na[n][a] for n in N_ for a in A_} #porcentaje de residuos que genera el alimento(sin ser consumido por el pez)
PC={(t,p): pc_p[t][p]for p in P_ for t in T_} #porcentaje de alimento que no es consumido por el pez
V={(t,s,p): peces_ingreso[t][s][p] for s in S_ for p in P_ for t in T_} # Peces p que ingresan a s en t
Y = {(s,t,a): alimentos_ingreso[t] for t in T_ for s in S_ for a in A_}

# ----------------------- Crear variables -------------------------
# Variables enteras (Las cambié a continuas para ver si pasaba algo)
X = model.addVars(S_, T_, P_, vtype=GRB.CONTINUOUS, name="X") #cantidad de peces que tiene la salmonera
CA = model.addVars(S_, T_, P_, A_, vtype=GRB.CONTINUOUS, name="CA") #cantidad de alimento que se le da al pez
Z  = model.addVars(S_,P_,T_, vtype=GRB.CONTINUOUS, name = "Z") #cantidad de peces comercializados
# Variables binarias
Q = model.addVars(S_, T_, vtype=GRB.BINARY, name="Q") # 1 si esque se pasa del tope permitido de externalidades, 0 en otro caso

# ------------------------ Crear restricciones --------------------

# 1) Flujo de peces (y caso base)
model.addConstrs((X[s,t,p] == V[t,s,p] + X[s,t-1,p] - Z[s,p,t-1] for s in S_ for p in P_ for t in T_ if t !=0), name="R2")
# Caso base:
model.addConstrs((X[s,0,p] == V[0,s,p] + PE[s,p] - Z[s,p,0] for s in S_ for p in P_ ), name="R2.1")

# 2) Flujo de alimento (y caso base)

model.addConstrs((quicksum(CA[s,t,p,a] for p in P_) == Y[s,t,a] - quicksum(CA[s,t-1,p,a] for p in P_) for s in S_ for a in A_ for t in T_ if t != 0), name="R3.1")

model.addConstrs((CA[s,0,p,a]  <= PA[a,s] + Y[s,0,a] for p in P_ for s in S_ for a in A_), name="R3.2") # No puedo dar más de lo que tengo
# 3) Capacidad máxima de salmonera
model.addConstrs((X[s,t,p] <=  (VOL[s] * MAP[p])/WP[p]  + Big_M * Q[s,t] for  p in P_ for t in T_ for s in S_ ) , name="R4")

# 4) Satisfacer la demanda
model.addConstrs((d[t,p] <= quicksum(Z[s,p,t] for s in S_) for p in P_ for t in T_), name="R5")

# 5) Activación de la multa (Esta restricción hace que el código se demore mucho)
model.addConstrs((quicksum(quicksum(CA[s,t,p,a] * (beta[n,p] * (1 - PC[t,p]) + CO[n,a] * PC[t,p]) for p in P_) for a in A_) <= TOP[t,s,n] + (Big_M * Q[s,t])for n in N_ for s in S_ for t in T_), name="R6")

#6) Respetar el mínimo nutricional
model.addConstrs((quicksum(CA[s,t,p,a] * epsilon[i,a] for a in A_) >= alpha[i,p] * (X[s,t,p]) /365 for s in S_ for t in T_ for p in P_ for i in I_), name="R7")

# 7) Sólo se pueden enviar peces disponibles (los "Madurados")
model.addConstrs((V[t, s, p] >= Z[s, p, t+1] for s in S_ for t in T_ if t + 1 <= len(T_) - 1 for p in P_), name="R9")
model.addConstrs((PE[s,p] >= Z[s, p, 0] for s in S_ for p in P_), name="R9.1")

# Naturaleza de las variables:

model.addConstrs((CA[s,t,p,a] >= 0 for s in S_ for a in A_ for t in T_ for p in P_), name="N1")

# --------------------- Crear función objetivo y resolver el modelo --------------
funcion_objetivo = (quicksum(quicksum(quicksum(quicksum(quicksum(CA[s,t,p,a] * ((beta[n,p] * (1 - PC[t,p]))+ (CO[n,a] * PC[t,p])+ Q[s,t]) for p in P_)for s in S_)for n in N_)for a in A_)for t in T_)) 
model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()

print(f"En total, la contaminación del fondo marítimo es {model.objVal} (Kg))\n")
# -------------------------------- Resultados---------------------------
s_x = ""
s_ca=""
s_z=""
s_q=""

for s in S_:
    for t in T_:
        s_q += str(Q[s,t].x) + "," + str(s) + "," + str(t) + "\n"

for t in T_:
    for s in S_:
        for p in P_:
            s_x += str(X[s, t, p].x) + "," + str(s) + "," + str(t) + "," + str(p) + "\n"
            s_z += str(Z[s, p, t].x) + "," + str(s) + "," + str(p) + "," + str(t) + "\n"

for t in T_:
    for s in S_:
        for p in P_:
            for a in A_:
                s_ca += str(CA[s, t, p,a].x )+ "," + str(s) + "," + str(t)+ "," + str(p)+ "," + str(a) + "\n"
                
with open("resultados/valores_x.csv", "w") as archivo:
    archivo.write("X,s,t,p\n")
    archivo.write(s_x)

with open("resultados/valores_CA.csv","w") as archivo:
    archivo.write("CA,s,t,p,a\n")
    archivo.write(s_ca)          

with open("resultados/valores_z.csv", "w") as archivo:
    archivo.write("Z,s,p,t\n")
    archivo.write(s_z)  
    
with open("resultados/valores_q.csv", "w") as archivo:
    archivo.write("Q,s,t\n")
    archivo.write(s_q)        
    
# -------------------------------- Análisis de sensibilidad ---------------------------
'''El análisis de sensibilidad se realizó en el archivo .py de cada parámetro de interés, debido a que
no nos funcionó el metodo constr.pi para obtener los precios duales y ver la variación del valor de la función
objetivo en caso de estos valores.

Con las variaciones de los parámetros, se analiza cómo fue la variación de la función objetivo, y en el informe se explica.'''
# # ----------------'------------------ Graficar Resultados obtenidos  --------------------------------------

# En caso de poseer la librería, se puede ejecutar esta parte del código para ver los gráficos con mayor detalle

# peces = list()
# alimento = list()
# peces_vendidos = list()
# tope=list()
# tiempo = list(t + 2025 for t in T_)

# for t in T_:
#     suma_x = 0
#     suma_z = 0
#     suma_comida = 0
#     suma_q=0
#     for s in S_:
#         suma_q+= Q[s,t].x
#         for p in P_:
#             suma_x += X[s,t,p].x
#             suma_z += Z[s,p,t].x
#             for a in A_:
#                 suma_comida += CA[s,t,p,a].x
#     peces.append(suma_x)
#     peces_vendidos.append(suma_z)
#     alimento.append(suma_comida)
#     tope.append(suma_q)

# fig, ax = plt.subplots(1, 2)

# ax[0].plot(tiempo, peces, "o--", color="blue")
# ax[0].set_title("$\sum_{t \in T, p \in P} X_{s,t,p}$")
# ax[0].set_ylabel("Peces almacenados")

# ax[1].plot(tiempo, peces_vendidos, "o--", color="red")
# ax[1].set_title("$\sum_{t \in T, p \in P} Z_{s,p,t}$")
# ax[1].set_ylabel("Peces exportados")
# plt.show()


# plt.plot(tiempo, alimento, "o--", color="green")
# plt.title("$\sum_{t \in T, p \in P, a \in A} CA_{s,t,p,a}$")
# plt.ylabel("Comida suministrada")   
# plt.show()

# plt.plot(tiempo, tope, "o--", color="gray")
# plt.xlabel("Años")
# plt.ylabel("Tope máximo")
# plt.title("$\sum_{s \in S}Q_{s,t}$")

# plt.show()
