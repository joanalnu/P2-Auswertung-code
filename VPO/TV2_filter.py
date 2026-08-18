import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 1. Theoretical Values
R = 10e3   # 10 kOhm
C = 10e-9  # 10 nF
f_g_theory = 1 / (2 * np.pi * R * C)

# Transfer Ratio Model Functions
def g_lowpass(f, fg):
    return 1 / np.sqrt(1 + (f / fg)**2)

def g_highpass(f, fg):
    return (f / fg) / np.sqrt(1 + (f / fg)**2)

# 2. Data Loading Function (Line by Line -> Numpy Array)
def load_data(filepath):
    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Skip the first two header lines ([source: 1], [source: 2])
        for line in lines[2:]:
            # Ignore completely empty lines
            if not line.strip():
                continue
            
            # Strip whitespaces, split by comma, and convert to floats
            row = [float(val) for val in line.strip().split(',')]
            parsed_data.append(row)
    
    # Convert list of lists to a numpy array
    data_array = np.array(parsed_data)
    
    # Optional: Sort the array by the first column (Frequency) just to be safe
    data_array = data_array[data_array[:, 0].argsort()]
    
    return data_array

# Load the data directly from your files
hp_data = load_data("TV2_hochpass_data.txt")
lp_data = load_data("TV2_tiefpass_data.txt")

# 3. Calculate Transfer Ratio |G| and Uncertainty
def calculate_g_and_dg(data):
    # Slice the numpy array by columns
    f = data[:, 0]
    U1 = data[:, 1]
    dU1 = data[:, 2]
    U2 = data[:, 3]
    dU2 = data[:, 4]
    
    # Calculate G and its error using Gaussian error propagation
    G = U2 / U1
    dG = G * np.sqrt((dU2 / U2)**2 + (dU1 / U1)**2)
    
    return f, G, dG

f_hp, G_hp, dG_hp = calculate_g_and_dg(hp_data)
f_lp, G_lp, dG_lp = calculate_g_and_dg(lp_data)

# 4. Fit Curves to Determine Experimental Cutoff Frequencies
popt_hp, _ = curve_fit(g_highpass, f_hp, G_hp, p0=[f_g_theory])
popt_lp, _ = curve_fit(g_lowpass, f_lp, G_lp, p0=[f_g_theory])

fg_hp_exp = popt_hp[0]
fg_lp_exp = popt_lp[0]

# 5. Plotting
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Generate a dense array of frequencies for a smooth fit curve
f_dense = np.linspace(50, 5500, 500)
freq_error = 0.05  # 0.5 Hz frequency error as stated in your task

# High Pass Plot
axes[0].errorbar(f_hp, G_hp, xerr=freq_error, yerr=dG_hp, fmt='o', color='blue', label='Messdaten')
axes[0].plot(f_dense, g_highpass(f_dense, fg_hp_exp), 'r-', label=f'Fit Curve ($f_g$ = {fg_hp_exp:.1f} Hz)')
axes[0].axvline(f_g_theory, color='grey', linestyle='--', label=f'Theorie $f_g$ ({f_g_theory:.1f} Hz)')
axes[0].axhline(1 / np.sqrt(2), color='green', linestyle=':', label=r'|G| = $1/\sqrt{2}$')
axes[0].set_title('Hochpass')
axes[0].set_xlabel('Frequenz $f$ [Hz]')
axes[0].set_ylabel('$|G| = U_2 / U_1$')
axes[0].grid(True)
axes[0].legend()

# Low Pass Plot
axes[1].errorbar(f_lp, G_lp, xerr=freq_error, yerr=dG_lp, fmt='o', color='blue', label='Messdaten')
axes[1].plot(f_dense, g_lowpass(f_dense, fg_lp_exp), 'r-', label=f'Fit Curve ($f_g$ = {fg_lp_exp:.1f} Hz)')
axes[1].axvline(f_g_theory, color='grey', linestyle='--', label=f'Theorie $f_g$ ({f_g_theory:.1f} Hz)')
axes[1].axhline(1 / np.sqrt(2), color='green', linestyle=':', label=r'|G| = $1/\sqrt{2}$')
axes[1].set_title('Tiefpass')
axes[1].set_xlabel('Frequenz $f$ [Hz]')
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()

# Print Comparison Output
print(f"Theoretische Grenzfrequenz: {f_g_theory:.2f} Hz")
print(f"Hochpass Experimentell Grenzfrequenz: {fg_hp_exp:.2f} Hz")
print(f"Tiefpass Experimentell Grequenzfrequenz: {fg_lp_exp:.2f} Hz")
