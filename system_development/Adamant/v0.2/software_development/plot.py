import functionFIles as ff  
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
import re
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
import os
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from itertools import combinations

def get_label(filepath, good_welds, bad_welds):
    match = re.search(r'Run(\d+)', filepath, re.IGNORECASE)
    if match:
        run_num = int(match.group(1))
        if run_num in good_welds:
            return "Good Weld"
        elif run_num in bad_welds:
            return "Bad Weld"
    return "Unknown"

plt.rcParams.update({
    "font.size": 11,
    "font.family": "Times New Roman",
})

ff.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Thermal Radiation CSV"

CSVFiles = ff.buildFilePaths(inputPath)

goodWelds = [4, 5, 7, 8, 10]
badWelds = [6, 9]

results = []
for filepath in CSVFiles:
    df = pd.read_csv(filepath, header=None)
    frame = df.values

    mask = frame > (0.5 * np.max(frame))
    results.append({
        "file": filepath,
        "label": get_label(filepath, goodWelds, badWelds),
        "mean": float(np.mean(frame)),
        "median": float(np.median(frame)),
        "standard deviation": float(np.std(frame)),
        "min": float(np.min(frame)),
        "max": float(np.max(frame)),
        "range": float(np.max(frame) - np.min(frame)),
        "skewness": float(skew(frame, axis=None)),
        "kurtosis": float(kurtosis(frame[mask], axis=None)),
        "mean_masked": float(np.mean(frame[mask]))
    })

results_df = pd.DataFrame(results)
print(results_df)

# Pearson coefficient plot 
    # Features to keep: features = ["mean", "std_dev", "max", "skewness", "kurtosis"]
# Logarithmic 2D classification: page 87 in the textbook


features = ["mean", "median", "standard deviation", "min", "max", "range", "skewness", "kurtosis", "mean_masked"]

os.makedirs(r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Plots", exist_ok=True)
outputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Plots"

for feat1, feat2 in combinations(features, 2):
    plt.figure()
    for label, group in results_df.groupby("label"):
        color = "green" if label == "Good Weld" else "red"
        plt.scatter(group[feat1], group[feat2], label=label, color=color)
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.title(f"{feat1} vs {feat2}")
    plt.legend()
    plt.savefig(rf"{outputPath}\{feat1}_vs_{feat2}.png", dpi=300, bbox_inches='tight')
    plt.savefig(rf"{outputPath}\{feat1}_vs_{feat2}.svg")
    plt.close()

featuresPearson = ["skewness", "kurtosis", "standard deviation", "max"]

corr = results_df[featuresPearson].corr()

# Rename for display only, on a copy
corr_display = corr.copy()
corr_display.index = ["skewness", "kurtosis", "standard\ndeviation", "max"]
corr_display.columns = ["skewness", "kurtosis", "standard\ndeviation", "max"]

plt.figure(figsize=(4, 3.25))
ax = sns.heatmap(
    corr_display,  # <-- use display copy here
    annot=True,
    fmt=".2f",
    cmap="viridis",
    center=0,
    vmin=-1,
    vmax=1,
    annot_kws={"size": 11}
)

colorbar = ax.collections[0].colorbar
colorbar.set_ticks([-1, -0.75, -0.50, -0.25, 0, 0.25, 0.50, 0.75, 1.0])
colorbar.set_label("Pearson correlation", size=11)

plt.tight_layout()
plt.savefig(rf"{outputPath}\correlation_matrix.png", dpi=300)
plt.savefig(rf"{outputPath}\correlation_matrix.svg")
plt.close()

featuresCorr = ["mean", "standard deviation", "max", "skewness", "kurtosis"]

for feat in featuresCorr:
    plt.figure()
    for label, group in results_df.groupby("label"):
        color = "green" if label == "Good Weld" else "red"
        sns.kdeplot(group[feat], label=label, color=color, fill=True, alpha=0.3)
    plt.xlabel(feat)
    plt.ylabel("Density")
    plt.title(f"Gaussian Distribution - {feat}")
    plt.legend()
    plt.savefig(rf"{outputPath}\kde_{feat}.png", dpi=300, bbox_inches='tight')
    plt.savefig(rf"{outputPath}\kde_{feat}.svg")
    plt.close()

feature_pairs = [
    ("standard deviation", "skewness"),
    ("standard deviation", "max"),
    ("skewness", "kurtosis"),
]

fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.25))

feature_pair_labels = [
    ("standard deviation", "skewness"),
    ("standard deviation", "max"),
    ("skewness", "kurtosis"),
]

for i, ((feat1, feat2), ax) in enumerate(zip(feature_pairs, axes)):
    x2 = results_df[[feat1, feat2]].values
    y2 = (results_df["label"] == "Good Weld").astype(int)

    scaler = StandardScaler()
    X2_scaled = scaler.fit_transform(x2)

    clf = LogisticRegression()
    clf.fit(X2_scaled, y2)

    x_min, x_max = X2_scaled[:, 0].min() - 1.5, X2_scaled[:, 0].max() + 1.5
    y_min, y_max = X2_scaled[:, 1].min() - 1.5, X2_scaled[:, 1].max() + 1.5

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 200),
        np.linspace(y_min, y_max, 200)
    )

    Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

    ax.contourf(xx, yy, Z, levels=[0, 0.5], colors=["#4C72B0"], alpha=0.2)
    ax.contourf(xx, yy, Z, levels=[0.5, 1], colors=["yellow"], alpha=0.2)

    contours = ax.contour(xx, yy, Z, levels=[0.1, 0.5, 0.9],
                          colors=["#4C72B0", "red", "green"])
    ax.clabel(contours, fmt="%.1f", fontsize=7)

    for label, group in results_df.groupby("label"):
        # Use standard matplotlib blue (#1f77b4) and orange (#ff7f0e)
        color = "#1f77b4" if label == "Good Weld" else "#ff7f0e"
        display_label = "good weld" if label == "Good Weld" else "bad weld"
        X_group = scaler.transform(group[[feat1, feat2]].values)
        ax.scatter(X_group[:, 0], X_group[:, 1], color=color,
                   label=display_label if i == 0 else "_nolegend_")

    # Spelled-out lowercase axis labels
    xlabel_str = feature_pair_labels[i][0]
    ylabel_str = feature_pair_labels[i][1]
    ax.set_xlabel(f"{xlabel_str}\n({chr(97+i)})", fontsize=11)
    ax.set_ylabel(ylabel_str, fontsize=11)

    # Enforce axis bounds
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

# Single legend on the first axis only
axes[0].legend(
    frameon=True,
    framealpha=1,
    facecolor="white",
    fontsize=8,
    markerscale=0.6,
    handlelength=1.0,
    handletextpad=0.4,
    borderpad=0.4,
    labelspacing=0.3,
)
fig.tight_layout()

fig.savefig(
    rf"{outputPath}\combined_boundary.jpg",
    dpi=300,
    facecolor="white",
    bbox_inches="tight"
)
fig.savefig(
    rf"{outputPath}\combined_boundary.svg",
    facecolor="white",
    bbox_inches="tight"
)

plt.close(fig)