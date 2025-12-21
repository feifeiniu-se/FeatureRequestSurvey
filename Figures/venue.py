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

journal_column = 'Journal'

# Ensure the venue/journal column exists
if journal_column not in df_filtered.columns:
    # If 'Journal' doesn't exist, try other common column names
    possible_columns = ['Conference', 'Venue', 'Publication', 'Source', 'Publisher']
    for col in possible_columns:
        if col in df_filtered.columns:
            journal_column = col
            break
    else:
        raise ValueError(
            f"Venue/journal column not found. Available columns: {df_filtered.columns.tolist()}"
        )

# Count venue/journal occurrences
journal_counts = df_filtered[journal_column].value_counts()

# Keep venues/journals that appear more than once
frequent_journals = journal_counts[journal_counts > 1].sort_values(ascending=False)

print(f"Venues/journals appearing more than once: {len(frequent_journals)}")
print(frequent_journals)

# Prepare data for plotting
journal_names = frequent_journals.index.tolist()
journal_values = frequent_journals.values.tolist()

# Plot
plt.figure(figsize=(max(20, len(journal_names) * 0.8), 8))

# Bar chart
bars = plt.bar(range(len(journal_names)), journal_values, width=0.8, color='#1f77b4', alpha=0.9)
# TODO: Currently single-color; uncomment below for multi-color and tweak as needed.
# colors = plt.cm.Dark2(np.linspace(0, 1, len(journal_names)))
# colors = plt.cm.tab20(np.linspace(0, 1, len(journal_names)))
# bars = plt.bar(range(len(journal_names)), journal_values, width=0.8, color=colors, alpha=0.9)


# Add value labels on top of bars
for i, bar in enumerate(bars):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', fontsize=18)

# Axis labels
plt.xlabel('Venue', fontsize=18, fontweight='bold')
plt.ylabel('Count', fontsize=18, fontweight='bold')

# X-axis labels (rotated for readability)
plt.xticks(range(len(journal_names)), journal_names, rotation=30, ha='right', fontsize=16)
plt.xlim(-0.5, len(journal_names) - 0.5)
plt.yticks(fontsize=16)

# Adjust Y-axis range
if journal_values:
    plt.ylim(0, max(journal_values) * 1.1)

# Remove outer frame
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
# plt.gca().spines['left'].set_visible(False)
# plt.gca().spines['bottom'].set_visible(False)

# Remove tick marks
plt.tick_params(axis='both', which='both', length=0)

# Layout
plt.tight_layout()

# Save as PDF
pdf_file_path = 'fig/venue.pdf'  # Replace with your desired output path/name
plt.savefig(pdf_file_path, format='pdf', dpi=600)

plt.show()
