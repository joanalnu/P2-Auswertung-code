import matplotlib.pyplot as plt
import numpy as np
from scipy.odr import ODR, Model, RealData

r = 1
# messreihe

# lesen der daten
with open(f"TV5_data_{r}.txt", 'r') as f:
    content = f.readlines()
    
    xlabel, ylabel = content[0].strip().split(",")
    xunit, yunit = content[1].strip().split(",")
    xdiv, ydiv = content[2].strip().split(",")
    xerr, yerr = (1/20) * float(xdiv), (1/20) * float(ydiv)

    xdata, ydata = [], []
    for line in content[3:]:
        x, y = line.strip().split(",")
        xdata.append(float(x))
        ydata.append(float(y))

xdata, ydata = np.array(xdata), np.array(ydata)

# push spannungen zu log-raum
ydata_log = np.log(ydata) # automatische basis "e"
yerr_log = yerr/ydata

# berechne ideale gerade (1/tau)
def linear_relation(P, x):
    return P[0] * x + P[1]

model = Model(linear_relation)
data = RealData(xdata, ydata_log, sx=xerr, sy=yerr_log)
odr = ODR(data, model, beta0=[1,0])
output = odr.run()
steigung, yachsenabschnitt = output.beta
delta_steigung = output.sd_beta[0]

print(fr"Steigung = {steigung:.5f}\pm {delta_steigung:.5f}")
print(f"y-Achsenabscnitt = {yachsenabschnitt:.3f}")

# berechne die werte fuer das plot
xgerade = np.linspace(min(xdata), max(xdata), 100)
ygerade = linear_relation((steigung, yachsenabschnitt), xgerade)

# erstelle abbildung

fig, ax = plt.subplots(figsize=(8,6))

ax.errorbar(xdata, ydata_log, xerr=xerr, yerr=yerr_log, fmt='o', markersize=4, label=fr"m = {steigung:.5f}±{delta_steigung:.5f} (Reihe {r})")
ax.plot(xgerade, ygerade, color='r')

ax.fill_between(xgerade, linear_relation((steigung-delta_steigung, yachsenabschnitt), xgerade), linear_relation((steigung+delta_steigung, yachsenabschnitt), xgerade), color='r', alpha=0.3)

plt.legend()
plt.title("Linearisierte Entladekurve eines Kondensators")
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.grid(True)
fig.savefig(f"TV5_plot_{r}.pdf", dpi=300)
fig.savefig("last_fig.png", dpi=300)
