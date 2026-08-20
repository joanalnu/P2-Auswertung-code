import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Bauteildaten
C = 10e-9 # F
L = 0.116 # H
R = 340   # Ohm

# lesen der Messdaten
with open("TV3_data.txt", 'r') as f:
    lines = f.readlines()

    f, U, div = list(), list(), list()

    for line in lines[2:]:
        a, b, c = line.strip().split(",")
        f.append(float(a))   #khz
        U.append(float(b))   #V
        div.append(float(c)) #V

# berechnung der Strom
I = [u/R for u in U]

delta_f = 0.05 # khz
delta_U = [d*(1/20) for d in div]
delta_I = [dU/R for dU in delta_U]

f = [freq*1000 for freq in f] # umrechnung kHz -> Hz
I = [i/1000 for i in I] # umrechnung A -> mA
delta_I = [dI/1000 for dI in delta_I]

def resonanz_kurve(f, I_max, f0, Q):
    # Frequenz, max Strom, Resonanzfrequenz, Güte
    return I_max / np.sqrt(1 + Q**2 * (f/f0 - f0/f)**2)

# optimale kurve berechnen
p0 = [max(I), 4250, 5] # I_max, f0, Q
popt, pcov = curve_fit(resonanz_kurve, f, I, p0=p0)
I_max_opt, f0_opt, Q_opt = popt
f0_err = np.sqrt(pcov[1,1])

# theoretische resonanzfrequenz
f0_theorie = 1/ (2 * np.pi * np.sqrt(L * C))
# gausssche fehlerfortpflanzung
f0_theorie_error = f0_theorie * 1/2 * np.sqrt(0.01**2 + 0.01**2)

print(f"Theoretische Resonanzfrequenz = ({f0_theorie:.2f} ± {f0_theorie_error:.2f}) Hz")
print(f"Experimentelle Resonanzfrequenz = ({f0_opt:.2f} ± {f0_err:.2f}) Hz")
# print(f"Imax = {I_max_opt} A;    Q = {Q_opt}")


# erstellung der abbildung
f_plot = np.linspace(min(f), max(f), 500)
I_plot = resonanz_kurve(f_plot, I_max_opt, f0_opt, Q_opt)

plt.figure(figsize=(8,5))
plt.errorbar(f, I, xerr=delta_f, yerr=delta_I, fmt='o', label="Messdaten", capsize=3)
plt.plot(f_plot, I_plot, '-', color='orange', label=f'Fit-Kurve ($f_0$ = {f0_opt:.0f} Hz)')
plt.axvline(f0_theorie, color='red', linestyle='--', label=f'Theorie ($f_0$ = {f0_theorie:.0f} Hz)')

plt.xlabel("Frequenz $f$ [kHz]")
plt.ylabel("Strom $I$ [A]")
plt.title("Resonanzkurve eines Serienschwingkreises")
plt.legend()
plt.grid(True)
plt.savefig("TV3_plot.pdf", dpi=300)
plt.savefig("preview.png", dpi=300)
