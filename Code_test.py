import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Constants
M = 29.0e-3
R = 8.31
P0 = 1.0e5
g0 = 9.8
RT = 6.4e3
RT_m = 6.4e6
pi = np.pi

zexp = np.array([0.0, 5.0, 10.0, 12.0, 20.0, 25.0, 30.0,35.0, 40.0,
                 45.0, 48.0, 52.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 84.0, 92.0, 95.0,100.0])

Texp = np.array([15.0, -18.0, -49.0, -56.0, -56.0, -51.0, -46.0, -37.0,
                 -22.0, -8.0, -2.0, -2.0, -7.0, -17.0, -33.0, -54.0, -65.0, -79.0, -86.0,-86.0, -81.0, -72.0])


# Fonction d'interpolation 
def T(z, unite):
    zkm = z / 1000 # Conversion en km pour comparaison dans la liste
    alpha = 1
    if unite == 'C':
        alpha = 0 # Pas de décalage pour la température en °C
    i = 0
    while zkm > zexp[i + 1]: # Recherche de l’indice i
        i = i + 1
    temperature = alpha*273 + Texp[i] + (zkm - zexp[i])/(zexp[i + 1] - zexp[i])*(Texp[i + 1] - Texp[i]) # Interpolation linéaire
    return temperature

# interpolations
N = 1000 # Nombre de points
zmax = 100.0e3 # Altitude max (en m)
dz = zmax/(N - 1) # Pas spatial (en m)
zatm = np.array([k*dz for k in range(N)]) # Altitudes
Tatm = np.array([T(zatm[k], 'C') for k in range(N)]) # Températures

# PLOT
fig, ax = plt.subplots()
ax.plot( Tatm,zatm)
plt.show()

# Champ de pesanteur
def g(z): # Champ de pesanteur
    return g0 * RT**2 / (RT + z)**2

# Calcul du champ de pression par la méthode d’Euler
Patm = [P0] # Initialisation
for k in range(N - 1): # Il reste N - 1 termes à calculer
    Patm.append(Patm[k] - M*g(zatm[k])*Patm[k]*dz/(R*T(zatm[k], 'K')))
Patm = np.array(Patm) # Conversion en tableau

fig, ax = plt.subplots()
ax.plot( Patm,zatm)
#plt.savefig("graph_Q7.png")
plt.show()

# calcul de la masse
def masse_atm(z): # Calcul de la masse d’air jusqu’à l’altitude z
    masse = 0
    k = 0
    while zatm[k] < z: # On arrête le calcul à l’altitude z
        dm = 4*np.pi*(RT_m+zatm[k])**2*M*Patm[k]/(R*T(zatm[k], 'K')) * dz
        masse = masse + dm
        k = k + 1
    return masse

mtropo10 = masse_atm(100e3) # Masse d'air dans la troposphère
print('Proportion d\'air dans la troposphère :', mtropo10)

mtropo12 = masse_atm(15e3) # Masse d'air dans la troposphère
print('Proportion d\'air dans la troposphère :', mtropo12)


Patm2 = [P0]
for k in range(N - 1):
    Patm2.append(Patm2[k] - M*g0*Patm2[k]*dz/(R*T(zatm[k], 'K')))
Patm2 = np.array(Patm2)
ecart1 = 100 * abs(Patm - Patm2) / Patm # Ecart relatif

fig, ax = plt.subplots()
ax.plot( Patm,zatm)
ax.plot( Patm2,zatm)
plt.show()
#plt.savefig("graph_Q13.png")
