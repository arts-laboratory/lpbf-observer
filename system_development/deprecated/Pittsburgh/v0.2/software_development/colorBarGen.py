import matplotlib.pyplot as plt
import matplotlib.colorbar as mcolorbar
import numpy as np
from pathlib import Path

outputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Footage"

plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots(figsize=(10, 1))
fig.subplots_adjust(bottom=0.5)

norm = plt.Normalize(vmin=20, vmax=900)
cb = mcolorbar.ColorbarBase(ax, cmap=plt.cm.inferno, norm=norm, orientation='horizontal')

cb.set_label('Temperature (°C)', fontsize = 11)
ax.tick_params(labelsize=12)

plt.savefig(str(Path(outputPath) / "colorbar.png"), bbox_inches='tight', dpi=300)
plt.close()