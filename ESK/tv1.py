import numpy as np
import matplotlib.pyplot as plt


# Teil A: Galvanische Zelle


# Laden der Daten
I_galv_mA = np.array([39.2, 29.1, 21.6, 20.4, 18.0, 16.0, 14.6, 13.3, 12.3, 11.0, 10.8])
U_galv_V  = np.array([1.108, 1.234, 1.162, 1.264, 1.288, 1.310, 1.325, 1.338, 1.349, 1.361, 1.366])

U_0_vorher = 1.181  # V am Anfang
U_0_nachher = 1.479 # V am Ende

# Lineare Regression (Ausgleichsgerade)
poly = np.polyfit(I_galv_mA, U_galv_V, 1)
steigung = poly[0] # V / mA
intercept = poly[1] # V

R_i = -steigung * 1000.0  # Ohm (weil I in *m*A)
U_q = intercept           # V

print(f"Steigung: {steigung:.6f} V/mA")
print(f"R_i: {R_i:.3f} Ohm")
print(f"Extrapolierte Leerlaufsp. (U_q, bei I=0): {U_q:.4f} V")

I_fit = np.linspace(0, 42, 100)
U_fit = steigung * I_fit + intercept

# erstellung des  plots
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(I_galv_mA, U_galv_V, color='#1f77b4', s=40, label='Messpunkte Belastung', zorder=3)
ax.plot(I_fit, U_fit, color='#d62728', linestyle='--', linewidth=1.8, 
         label=f'Ausgleichsgerade ($R_i = {R_i:.2f}\\,\\Omega$, $U_q = {U_q:.3f}\\,\\mathrm{{V}}$)')

# Punkte bei I = 0 eintragen
ax.plot(0, U_q, 'ro', label=f'Extrapoliertes $U_q = {U_q:.3f}\\,\\mathrm{{V}}$')
ax.plot(0, U_0_vorher, 'go', label=f'Gemessen $U_{{0,\\mathrm{{vorher}}}} = {U_0_vorher:.3f}\\,\\mathrm{{V}}$')

ax.set_xlabel('Belastungsstrom $I$ [mA]')
ax.set_ylabel('Klemmenspannung $U$ [V]')
ax.set_title('Belastungskennlinie der galvanischen Zelle')
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='lower left', frameon=True)
plt.savefig('tv1_galvanisch.pdf', dpi=300)
plt.savefig('last_fig.png', dpi=300)
plt.close()




# TEIL B: Netzgereat


U_ng_V = np.array([10.19, 10.19, 10.19, 10.19, 10.18, 10.18, 10.17, 10.16, 10.15, 10.12, 10.05])
I_multi_mA = np.array([100.3, 111.5, 123.7, 139.4, 161.5, 184.6, 218.6, np.nan, np.nan, np.nan, np.nan])
I_zange_A  = np.array([0.122, 0.134, 0.146, 0.162, 0.177, 0.200, 0.233, 0.285, 0.352, 0.498, 0.846])
I_zange_mA = I_zange_A * 1000.0

# erstellung des  plots
fig, ax = plt.subplots(figsize=(6.5, 4.2))

ax.plot(I_zange_mA, U_ng_V, 'o-', color='#2ca02c', label='Messung Stromzange')
valid_m = ~np.isnan(I_multi_mA)
ax.plot(I_multi_mA[valid_m], U_ng_V[valid_m], 's-', color='#ff7f0e', label='Messung Multimeter')

ax.set_xlabel('Belastungsstrom $I$ [mA]')
ax.set_ylabel('Klemmenspannung $U$ [V]')
ax.set_title('Belastungskennlinie des stabilisierten Netzgeräts')
ax.set_ylim(9.90, 10.30)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='lower left', frameon=True)
plt.tight_layout()
plt.savefig('tv1_netzgeraet.pdf', dpi=300)
plt.savefig('last_fig.png', dpi=300)
plt.close()

