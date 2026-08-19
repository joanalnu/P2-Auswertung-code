import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Parameter der Komponente
R = 10e3   # 10 kOhm
C = 10e-9  # 10 nF
fg_theorie = 1 / (2 * np.pi * R * C) # theoretische Grenzfrequenz $f_z$
# gausssche fehlerfortpflanzung; beide sind pm 1%
fg_theorie_error = fg_theorie * np.sqrt(0.01**2 + 0.01**2)

def g_tiefpass(f, fg):
    return 1/ np.sqrt(1 + (f/fg)**2)

def g_hochpass(f, fg):
    return (f/fg) / np.sqrt(1 + (f/fg)**2)

# lesen der Daten
def load_data(path):
    data = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines[2:]:
            row = [float(val) for val in line.strip().split(',')]
            data.append(row)

    return np.array(data) # convert to array

hp_data = load_data("TV2_hochpass_data.txt")
tp_data = load_data("TV2_tiefpass_data.txt")


# Berechnung des Übertragungsverhältnis |G| (Betrag)
def calculate_g(data):
    f = data[:, 0] # frequenz
    U1 = data[:, 1] # Spannung Kanal 1
    dU1 = data[:, 2]
    U2 = data[:, 3] # Spannung Kanal 2
    dU2 = data[:, 4]
    
    G = U2/U1
    dG = G * np.sqrt((dU2/U2)**2 + (dU1/U1)**2)

    return f, G, dG

f_hp, G_hp, dG_hp = calculate_g(hp_data)
f_tp, G_tp, dG_tp = calculate_g(tp_data)


# berechnung der optimale Kurven
popt_hp, pcov_hp = curve_fit(g_hochpass, f_hp, G_hp, p0=[fg_theorie])
popt_tp, pcov_tp = curve_fit(g_tiefpass, f_tp, G_tp, p0=[fg_theorie])

fg_hp = popt_hp[0]
fg_tp = popt_tp[0]

fg_hp_error = np.sqrt(np.diag(pcov_hp))[0]
fg_tp_error = np.sqrt(np.diag(pcov_tp))[0]

# erstellung der abbildung
fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12,5))

# x-achse fur die optimale gerade
f_fit = np.linspace(50, 5500, 500)
freq_error = 0.5  # Hz

# Tiefpass (links)
axes[0].errorbar(f_tp, G_tp, xerr=freq_error, yerr=dG_tp, fmt='o', color='blue', label='Messdaten')
axes[0].plot(f_fit, g_tiefpass(f_fit, fg_tp), 'r-', label=f'optimale Kurve ($f_g$ = {fg_tp:.1f} Hz)')
axes[0].axvline(fg_theorie, color='grey', linestyle='--', label=f'Theorie $f_g$ ({fg_theorie:.1f} Hz)')
axes[0].axhline(1 / np.sqrt(2), color='green', linestyle=':', label=r'|G| = $1/\sqrt{2}$')
axes[0].set_title('Tiefpass')
axes[0].set_xlabel('Frequenz $f$ [Hz]')
axes[0].grid(True)
axes[0].legend()

# Hochpass (rechts)
axes[1].errorbar(f_hp, G_hp, xerr=freq_error, yerr=dG_hp, fmt='o', color='blue', label='Messdaten')
axes[1].plot(f_fit, g_hochpass(f_fit, fg_hp), 'r-', label=f'Fit Curve ($f_g$ = {fg_hp:.1f} Hz)')
axes[1].axvline(fg_theorie, color='grey', linestyle='--', label=f'Theorie $f_g$ ({fg_theorie:.1f} Hz)')
axes[1].axhline(1 / np.sqrt(2), color='green', linestyle=':', label=r'|G| = $1/\sqrt{2}$')
axes[1].set_title('Hochpass')
axes[1].set_xlabel('Frequenz $f$ [Hz]')
axes[1].set_ylabel('$|G| = U_2 / U_1$')
axes[1].grid(True)
axes[1].legend()

fig.savefig("TV2_plot.pdf", dpi=300)
fig.savefig("preview.png", dpi=300)

# Print Comparison Output
print(f"Theoretische Grenzfrequenz: ({fg_theorie:.2f} ± {fg_theorie_error:.2f}) Hz")
print(f"Hochpass Experimentell Grenzfrequenz: ({fg_hp:.2f} ± {fg_hp_error:.2f}) Hz")
print(f"Tiefpass Experimentell Grequenzfrequenz: ({fg_tp:.2f} ± {fg_tp_error:.2f}) Hz")
