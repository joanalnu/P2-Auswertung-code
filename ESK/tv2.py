import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData

# laden von daten
U_V = np.array([0.00, 2.05, 4.02, 6.00, 8.04, 9.93, 11.93, 14.01, 15.90, 17.93, 19.80])
I_mA = np.array([0.00, 0.50, 1.22, 1.82, 2.45, 3.04, 3.64, 4.28, 4.85, 5.47, 6.04])

I_A = I_mA / 1000.0 # mA -> A

# fuer die fehlerbestimmung der ausgleichsgerade
err_U = (0.009 * U_V) + (4 * 0.01)
err_I_mA = (0.018 * I_mA) + (5 * 0.01)
err_I_A = err_I_mA / 1000.0

def ohms_law(B, x):
    return B[0] * x # R * I

model = Model(ohms_law)
data = RealData(I_A, U_V, sx=err_I_A, sy=err_U)

odr_obj = ODR(data, model, beta0=[3300.0])
output = odr_obj.run()

# Extract calculated Resistance and its standard error
R_calculated = output.beta[0]
R_calculated_err = output.sd_beta[0]

# Farben (hersteller)
R_color = 3300.0 # Ohms
R_color_err = R_color * 0.01

# Multimeter (messung)
R_multi = 3280.0 # Ohms (3.28 kOhm)
R_multi_err = (0.01 * R_multi) + (8 * 10)

# erstellung des plots
plt.figure(figsize=(10, 6))

plt.errorbar(I_A, U_V, xerr=err_I_A, yerr=err_U, fmt='ko', label='Gemessene Werte', capsize=4)

I_fit = np.linspace(0, max(I_A) * 1.05, 100)
plt.plot(I_fit, ohms_law([R_calculated], I_fit), 'r-', label=f'Linearer Fit (R = {R_calculated:.0f} ± {R_calculated_err:.0f} $\\Omega$)')

plt.title('U-I Diagramm zur Bestimmung des Widerstands')
plt.xlabel('Strom $I$ [A]')
plt.ylabel('Spannung $U$ [V]')
plt.grid(True)
plt.legend()
plt.savefig('tv2_plot.pdf', dpi=300)
plt.savefig('last_fig.png', dpi=300)

print(f"1. Aus Diagramm (Fit):    {R_calculated:7.2f} +/- {R_calculated_err:5.2f} Ohm")
print(f"2. Hersteller (Farben):   {R_color:7.2f} +/- {R_color_err:5.2f} Ohm")
print(f"3. Multimeter (direkt):   {R_multi:7.2f} +/- {R_multi_err:5.2f} Ohm")
