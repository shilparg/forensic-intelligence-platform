import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Loading comprehensive forensic dataset...")
# 1. Load the master dataset you just created
df = pd.read_csv("comprehensive_forensic_dataset.csv")

# 2. Isolate only the numerical columns
# Heatmaps can only calculate math on numbers, so we drop text columns like 'ticker'
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# 3. Calculate the correlation matrix
# This calculates how strongly every single variable moves in relation to every other variable
corr_matrix = numeric_df.corr()

# 4. Set up the visual canvas
plt.figure(figsize=(14, 10))
plt.title("Forensic Triangulation: SEC Sentiment vs. Market Reality", fontsize=16, pad=20)

# 5. Generate the Heatmap
# We use a 'coolwarm' color map: Deep Red = Strong Positive Correlation, Deep Blue = Strong Negative
sns.heatmap(
    corr_matrix, 
    annot=True,        # Prints the exact correlation number inside each box
    fmt=".2f",         # Rounds the numbers to 2 decimal places
    cmap="coolwarm",   # The color scheme
    vmin=-1, vmax=1,   # Locks the mathematical scale from -1.0 to 1.0
    center=0,          # Centers the white color at exactly zero (no correlation)
    linewidths=0.5,    # Adds clean grid lines
    cbar_kws={"shrink": .8} # Slightly shrinks the color legend for better formatting
)

# 6. Show the visual
plt.tight_layout()
print("Generating Heatmap... Check your popped-up window!")
plt.show()