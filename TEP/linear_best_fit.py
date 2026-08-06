import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.odr import ODR, Model, Data

# parameter
TV = 4

titles = [
        "", # TV1
        "", # TV2
        "", # TV3
        "", # TV4
        "", # TV5
        ]

def lineare_relation(P, x):
    # steigung * x + yachsenabschnitt
    return P[0] * x + P[1]
model = Model(lineare_relation)

# importieren der Daten aus der CSV Dateien

with open(f"TV{TV}_data.txt", "r") as f:
    content = f.readlines()
    xlabel, ylabel = content[0].split(",")
    xunit, yunit = content[1].split(",")
    xdata, ydata = list(), list()

    for line in content[2:]:
        x,y = line.split(",")
        xdata.append(float(x))
        ydata.append(float(y))


# berechne die ideale Gerade
data = Data(xdata, ydata)
odr = ODR(data, model, beta0=[1, 0])
output = odr.run()

steigung, yachsenabschnitt = output.beta

print(f"Steigung = {steigung:.3f}")
print(f"y-Achsenabscnitt = {yachsenabschnitt:.3f}")
print(f"1/steigung = {1/steigung:.3f} (abs Temp)")

# berechne die werte fuer das plot
xgerade = np.linspace(min(xdata), max(xdata))
ygerade = lineare_relation((steigung, yachsenabschnitt), xgerade)

# erstellung des visuellen plots
fig, ax = plt.subplots()
ax.scatter(xdata, ydata)
ax.plot(xgerade, ygerade, label=f"")
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_title(titles[TV-1])
fig.savefig(f"TV{TV}_plot.pdf", dpi=300)
fig.savefig(f"last_fig.png", dpi=300)
