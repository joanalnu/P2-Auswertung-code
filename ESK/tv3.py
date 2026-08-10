import matplotlib.pyplot as plt
import numpy as np


# TEIL A: Draht

# Data for Teilversuch 3a: Spannungsabfall am Draht
laenge_cm = np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0])
spannung_draht_v = np.array([12.75, 11.63, 10.46, 9.10, 7.69, 6.59, 5.25, 3.96, 2.60, 1.29, 0])

# Plot 3a
plt.figure(figsize=(8, 6))
plt.plot(laenge_cm, spannung_draht_v, 'go', label='Messwerte (Draht)')
m_a, b_a = np.polyfit(laenge_cm, spannung_draht_v, 1)
plt.plot(laenge_cm, m_a * laenge_cm + b_a, 'r--', label=f'Linearer Fit')

plt.title('Teilversuch 3a: Spannungsabfall am Draht')
plt.xlabel('Länge [cm]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()
plt.savefig('tv3a.pdf', dpi=300)
plt.savefig('last_fig.png')
plt.close()




# TEIL B: Helipot

helipot_skt = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
spannung_u_v = np.array([0.09, 1.00, 2.01, 3.01, 4.01, 5.00, 6.00, 6.99, 8.00, 8.98, 9.95])
fehler_skt = 0.5 # fehler von Helipot

plt.figure(figsize=(8, 6))
plt.errorbar(helipot_skt, spannung_u_v, xerr=fehler_skt, fmt='bo', label='Messwerte (Helipot)', capsize=3)

# ausgleichsgerade
m_b, b_b = np.polyfit(helipot_skt, spannung_u_v, 1)
plt.plot(helipot_skt, m_b * helipot_skt + b_b, 'r--', label=f'Linearer Fit ($U = {m_b:.5f} \\cdot Skt + {b_b:.4f}$)')

plt.title('Ausgangsspannung des Helipots gegen Skalenwerte')
plt.xlabel('Skalenwert [Skt]')
plt.ylabel('Ausgangsspannung $U$ [V]')
plt.grid(True)
plt.legend()
plt.savefig('tv3b.pdf', dpi=300)
plt.savefig('last_fig.png')
plt.close()
