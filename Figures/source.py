import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
file_path = './source.xlsx'
df = pd.read_excel(file_path)

# Extract data
types = df['Types']
counts = df['count']

# Choose colors
colors = plt.get_cmap('tab20').colors  # Use a distinct colormap


# Set font
plt.rcParams['font.family'] = 'Times New Roman'

# Create the pie chart
fig, ax = plt.subplots(figsize=(8, 8))
# Draw the pie chart
wedges, _ = ax.pie(counts,
                   labels=[''] * len(types),
                   startangle=90,
                   counterclock=False,
                   colors=colors,
                   wedgeprops=dict(width=0.6))  # Donut width

# Add count labels
for i, wedge in enumerate(wedges):
    # Mid-angle of the wedge (degrees)
    angle = (wedge.theta2 + wedge.theta1) / 2
    # Convert degrees to radians
    x = 0.7 * np.cos(np.deg2rad(angle))
    y = 0.7 * np.sin(np.deg2rad(angle))
    ax.text(x, y, str(counts[i]), ha='center', va='center', fontsize=16)

# patches, texts, autotexts = plt.pie(
#     counts,
#     labels=[''] * len(types),  # Hide labels
#     colors=colors[:len(types)],
#     autopct=lambda pct: '{:.0f}'.format(pct * sum(counts) / 100),  # Show counts
#     textprops={'fontname': 'Times New Roman', 'fontsize': 14}
# )

# Add legend
ax.legend(wedges, types, loc="center left", bbox_to_anchor=(1, 0.5),
          fontsize=14, prop={'family': 'Times New Roman', 'size': 14})


# plt.title('Distribution of Types', fontname='Times New Roman', fontsize='16')
plt.tight_layout()

plt.savefig('fig/source.pdf', format='pdf', dpi=600)

plt.show()


# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Read the Excel file
# file_path = './source.xlsx'
# df = pd.read_excel(file_path)
#
# # Extract data
# types = df['Types']
# counts = df['count']
#
# # Choose colors
# colors = [
#     '#1f77b4',  # Blue
#     '#ff7f0e',  # Orange
#     '#2ca02c',  # Green
#     '#d62728',  # Red
#     '#9467bd',  # Purple
#     '#8c564b',  # Brown
#     '#e377c2',  # Pink
#     '#7f7f7f',  # Gray
#     '#bcbd22',  # Olive
#     '#17becf'   # Cyan
# ]
#
# # Set font
# plt.rcParams['font.family'] = 'Times New Roman'
#
# # Create the pie chart
# plt.figure(figsize=(8, 8))
# patches, texts, autotexts = plt.pie(
#     counts,
#     labels=[''] * len(types),  # Hide labels
#     colors=colors[:len(types)],
#     autopct=lambda pct: '{:.0f}'.format(pct * sum(counts) / 100),  # Show counts
#     textprops={'fontname': 'Times New Roman', 'fontsize': 14}
# )
#
# # Add legend
# plt.legend(
#     patches,
#     types,
#     loc="center left",
#     bbox_to_anchor=(1, 0.5),
#     prop={'family': 'Times New Roman', 'size': 14}
# )
#
# plt.title('Distribution of Types', fontname='Times New Roman', fontsize='16')
# plt.tight_layout()
#
# plt.savefig('fig/source.pdf', format='pdf', dpi=600)
#
# plt.show()
