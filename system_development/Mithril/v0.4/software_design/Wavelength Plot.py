import numpy as np
import matplotlib.pyplot as plt

# Set font to Times New Roman
plt.rcParams["font.family"] = "Times New Roman"

# Wavelength range
wavelength = np.linspace(500, 1200, 2000)

# ---- Create Data Arrays ----

# Filter: rises at 620 nm, peaks at 660 nm, drops to 0 at 720 nm
filter_intensity = np.zeros_like(wavelength)
rise_region = (wavelength >= 620) & (wavelength <= 660)
fall_region = (wavelength > 660) & (wavelength <= 720)

filter_intensity[rise_region] = (wavelength[rise_region] - 620) / (660 - 620)
filter_intensity[fall_region] = (720 - wavelength[fall_region]) / (720 - 660)

# Light: Gaussian peak at 625 nm
light_intensity = np.exp(-0.5 * ((wavelength - 625) / 15)**2)
light_intensity /= np.max(light_intensity)

# Laser: Narrow Gaussian peak at 1070 nm
laser_intensity = np.exp(-0.5 * ((wavelength - 1070) / 10)**2)
laser_intensity /= np.max(laser_intensity)

# Glass: Slightly wider Gaussian peak at 1070 nm
glass_intensity = np.exp(-0.5 * ((wavelength - 1070) / 25)**2)
glass_intensity /= np.max(glass_intensity)

# ---- Plot ----
plt.figure(figsize=(6.5, 3.5))
point = 12
plt.plot(wavelength, filter_intensity, label="Filter", linestyle="dotted", linewidth=2)
plt.plot(wavelength, light_intensity, label="Lights", linewidth=2)
plt.plot(wavelength, laser_intensity, label="Laser", linewidth=2)
plt.plot(wavelength, glass_intensity, label="Glass", linestyle="dotted", linewidth=2)

plt.xlim(500, 1200)
plt.ylim(0, 1)
plt.yticks([0, 0.5, 1])

plt.xlabel("Wavelength (nm)", fontsize=point)
plt.ylabel("Relative Intensity", fontsize=point)
plt.title("Wavelength vs Relative Intensity", fontsize=point)

plt.legend(loc="upper center")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig('wavelengths.svg')

plt.show()