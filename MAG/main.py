import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, RealData, Model


# Unsicherheiten
da = 2.0 # grad, unsicherheit von alpha
db = 0.5 # grad, unsicherheit von beta

# lesen der daten
with open('TV2_data.txt', 'r') as f:
    content = f.readlines()

    xlabel, ylabel = content[0].split(",")

    a, b = list(), list()
    for line in content[2:]:
        x,y = line.split(',')
        a.append(float(x))
        b.append(float(y))

    a = np.array(a)
    b = np.array(b)

# berechnung von phi (torsionswinkel)
# waehrend die messung wurde die 0 achse druchgegangen, die folgenden linie entfernt der sprung und betrachtet die inkremente zwischen winkel
beta = np.unwrap(np.asarray(b), period=360)

beta0 = beta[0]
phi = beta - beta0

dphi = [db * np.sqrt(2) for _ in range(len(phi))]

# berechnung des sinus
alpha = np.deg2rad(a) # von grad zu RADIANS
sinalpha = np.sin(alpha)

dalpha = [np.deg2rad(da) for _ in range(len(alpha))]
dsinalpha = np.sin(dalpha)

# berechnung der optimalen geraden (hoffentlich ursprungsgerade)

# entfernung des punktes (0,0) von den Daten, sonst verf√§lschung
sinalpha = sinalpha[1:]
dsinalpha = dsinalpha[1:]
phi = phi[1:]
dphi = dphi[1:]

def linear(P, x):
    return P[0] *x + P[1]

print("sinalpha", sinalpha)
print("dsinalpha", dsinalpha)
print("phi", phi)
print("dphi", dphi)

model = Model(linear)
data = RealData(sinalpha, phi, sx=dsinalpha, sy=dphi)
odr = ODR(data, model, beta0=[1,0])
output = odr.run()

steigung, yachsenabschnitt = output.beta
ds, dy = output.sd_beta

print(f"Steigung: {steigung:.2f} ± {ds:.2f}")
print(f"y-achsenabschnitt: {yachsenabschnitt:.2f} ± {dy:.2f}")


# erstellung der abbildung
sina_plot = np.linspace(0, max(sinalpha), 100)
phi_plot = linear((steigung, yachsenabschnitt), sina_plot)

fig, ax= plt.subplots(figsize=(8,5))
ax.errorbar(sinalpha, phi, xerr=dsinalpha, yerr=dphi, fmt='o', capsize=3, label="Messwerte")
ax.plot(sina_plot, phi_plot, '--', color='red', label=f"optimale lineare Gerade ($y_0 = $ {yachsenabschnitt:.2f} ± {dy:.2f})")

ax.set_xlabel(r"$\sin(\alpha)$")
ax.set_ylabel(r"$\varphi$ \ deg")
ax.set_title("Drehmoment des Feldes auf eine stromdurchflossene Spule")
ax.legend()
ax.grid(True)

fig.savefig("TV2_plot.pdf", dpi=300)
fig.savefig("last_fig.png", dpi=300)
