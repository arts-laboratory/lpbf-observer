import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import math
import os
import functionFIles as ff

ff.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Footage\Frames"
outputPath = r"C:\Users\mayhe\Dropbox\Hoang_2026_QNDE_Battery_welding\makingFigures\thermalImages"

chosenFrames = [(4, 675), (5, 455), (6, 313), (7, 282), (8, 583), (9, 388), (10, 331)]
imagePaths = [os.path.join(inputPath, f"Run{weld}.raviPeakFrame{frame}.png") for weld, frame in chosenFrames]
labels = [f"({chr(ord('a') + n - 1)}) sample {weld}" for n, (weld, frame) in enumerate(chosenFrames, start=1)]
colorBarPath = r"C:\Users\mayhe\Dropbox\Hoang_2026_QNDE_Battery_welding\makingFigures\thermalImages\colorbar.png"

output_file = os.path.join(outputPath, f"thermalImages.png")   # Output filename
n_cols     = 4              # Number of columns in the grid
dpi        = 300             # Resolution (300 = publication quality)
title_size = 11             # Font size for titles
fig_title  = ""    

plt.rcParams.update({
    "font.size": 11,
    "font.family": "Times New Roman",
})          # Optional overall figure title (or leave "")

n_images = len(chosenFrames)
n_rows   = math.ceil(n_images / n_cols)

colN = 1.5 * n_cols
rowN = 1 + 1.5 * n_rows

# Switch to GridSpec to accommodate colorbar row
fig = plt.figure(figsize=(colN, rowN))  # +1 for colorbar height

gs = gridspec.GridSpec(
    n_rows + 1, n_cols,
    figure=fig,
    height_ratios=[.1] + [1] * n_rows,
    hspace=0.05,   # ← very tight vertical spacing
    wspace=0.02,   # ← very tight horizontal spacing
)

# ── Colorbar at top spanning all columns ──────────────────────────────────────
ax_cb = fig.add_subplot(gs[0, :])
ax_cb.imshow(mpimg.imread(colorBarPath))
ax_cb.axis("off")

# ── Image grid ────────────────────────────────────────────────────────────────
axes = []
for i in range(n_rows * n_cols):
    row = i // n_cols + 1  # +1 to skip colorbar row
    col = i % n_cols
    axes.append(fig.add_subplot(gs[row, col]))

for i, (img_path, label) in enumerate(zip(imagePaths, labels)):
    img = mpimg.imread(img_path)
    axes[i].imshow(img)
    axes[i].set_xlabel(
        label,
        fontsize=title_size,
        labelpad=8,
        loc="center"
    )
    axes[i].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

# Hide unused slots
for j in range(n_images, len(axes)):
    axes[j].set_visible(False)

if fig_title:
    fig.suptitle(fig_title, fontsize=title_size + 4, fontweight="bold", y=1.02)

plt.savefig(output_file, dpi=dpi, bbox_inches="tight", format="jpeg")
plt.close()
print(f"Saved → {output_file}")
print(f"image Dimentions: {colN} x {rowN}")
