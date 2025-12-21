import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Global font setup: Times New Roman (bold optional)
plt.rcParams['font.family'] = 'Times New Roman'
# plt.rcParams['font.weight'] = 'bold'

# Read the Excel file
file_path = './vice.xlsx'  # Replace with your Excel file path
sheet_name = 'Year'  # Replace with your worksheet name (if needed)

# Load data from the Excel worksheet
# df = pd.read_excel(file_path,  header=0)
df = pd.read_excel(file_path, sheet_name=sheet_name)
print(df.columns)

# Ensure the "Year" column exists
if 'Year' not in df.columns:
    raise ValueError("Column 'Year' was not found in the Excel file")

# Ensure the "recheck" column exists
if 'recheck' not in df.columns:
    raise ValueError("Column 'recheck' was not found in the Excel file")

# Filter rows where recheck == 1
df_filtered = df[df['recheck'] == 1].copy()

# Ensure Year is integer
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
df_filtered = df_filtered.dropna(subset=['Year'])
df_filtered['Year'] = df_filtered['Year'].astype(int)

# Get filtered Year data
years = df_filtered['Year']

# Count year distribution
year_counts = years.value_counts().sort_index()

# Get min/max year in the data
min_year = year_counts.index.min()
max_year = year_counts.index.max()

# Plot
plt.figure(figsize=(12, 4))

# Bar chart
bars = plt.bar(year_counts.index, year_counts.values, width=0.8, color='#ff7f0e', alpha=0.9)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', fontsize=16)

# Axis labels
plt.xlabel('Year', fontsize=14, fontweight='bold')
# plt.ylabel('Cumulative Number of Benchmarks', fontsize=14, fontweight='bold')
# plt.title('Year Distribution with Bar and Line Charts', fontsize=16, fontweight='bold')

# Set X-axis range and ticks to show all bars
plt.xlim(min_year - 0.5, max_year + 0.5)
plt.xticks([year for year, count in zip(year_counts.index, year_counts.values) if count > 0], fontsize=14)  # Only show years with count > 0
plt.yticks(fontsize=14)
# Remove outer frame
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
# plt.gca().spines['bottom'].set_visible(False)

# Remove tick marks
plt.tick_params(axis='both', which='both', length=0)

# Layout
plt.tight_layout()

# Save as PDF
pdf_file_path = 'fig/year.pdf'  # Replace with your desired output path/name
plt.savefig(pdf_file_path, format='pdf', dpi=600)

plt.show()
