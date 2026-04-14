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
        "std_dev": float(np.std(frame)),
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


features = ["mean", "median", "std_dev", "min", "max", "range", "skewness", "kurtosis", "mean_masked"]

os.makedirs(r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Plots", exist_ok=True)

for feat1, feat2 in combinations(features, 2):
    plt.figure()
    for label, group in results_df.groupby("label"):
        color = "green" if label == "Good Weld" else "red"
        plt.scatter(group[feat1], group[feat2], label=label, color=color)
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.title(f"{feat1} vs {feat2}")
    plt.legend()
    plt.savefig(f"C:\\Users\\mayhe\\OneDrive\\Documents\\GitHub\\Dataset-battery-tab-laser-welding\\data\\Dataset-1\\Plots\\{feat1}_vs_{feat2}.png", dpi=300, bbox_inches='tight')
    plt.close()

corr = results_df[features].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="viridis", center=0)
plt.title("Pearson Correlation Matrix")
plt.tight_layout()
plt.savefig(r"C:\\Users\\mayhe\\OneDrive\\Documents\\GitHub\\Dataset-battery-tab-laser-welding\\data\\Dataset-1\\Plots\\correlation_matrix.png", dpi=300)
plt.close()

featuresCorr = ["mean", "std_dev", "max", "skewness", "kurtosis"]

for feat in featuresCorr:
    plt.figure()
    for label, group in results_df.groupby("label"):
        color = "green" if label == "Good Weld" else "red"
        sns.kdeplot(group[feat], label=label, color=color, fill=True, alpha=0.3)
    plt.xlabel(feat)
    plt.ylabel("Density")
    plt.title(f"Gaussian Distribution - {feat}")
    plt.legend()
    plt.savefig(f"C:\\Users\\mayhe\\OneDrive\\Documents\\GitHub\\Dataset-battery-tab-laser-welding\\data\\Dataset-1\\Plots\\kde_{feat}.png", dpi=300, bbox_inches='tight')
    plt.close()

for feat1, feat2 in combinations(featuresCorr, 2):
    x2 = results_df[[feat1, feat2]].values
    y2 = (results_df["label"] == "Good Weld").astype(int)

    scaler = StandardScaler()
    X2_scaled = scaler.fit_transform(x2)

    clf = LogisticRegression()
    clf.fit(X2_scaled, y2)

    x_min, x_max = X2_scaled[:, 0].min() - 1, X2_scaled[:, 0].max() + 1
    y_min, y_max = X2_scaled[:, 1].min() - 1, X2_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))

    Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

    plt.figure()
    plt.contourf(xx, yy, Z, levels=[0, 0.5], colors=["blue"], alpha=0.2)
    plt.contourf(xx, yy, Z, levels=[0.5, 1], colors=["yellow"], alpha=0.2)
    contours = plt.contour(xx, yy, Z, levels=[0.1, 0.5, 0.9], colors=["blue", "red", "green"])
    plt.clabel(contours, fmt="%.1f", fontsize=11)

    for label, group in results_df.groupby("label"):
        color = "green" if label == "Good Weld" else "red"
        X_group = scaler.transform(group[[feat1, feat2]].values)
        plt.scatter(X_group[:, 0], X_group[:, 1], label=label, color=color)

    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.title(f"2D Decision Boundary - {feat1} vs {feat2}")
    plt.legend()
    plt.savefig(f"C:\\Users\\mayhe\\OneDrive\\Documents\\GitHub\\Dataset-battery-tab-laser-welding\\data\\Dataset-1\\Plots\\boundary_{feat1}_vs_{feat2}.png", dpi=300, bbox_inches='tight')
    plt.close()