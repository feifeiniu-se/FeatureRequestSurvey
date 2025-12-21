import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Read the Excel file (update the path as needed)
file_path = './vice.xlsx'  # Replace with your actual file path
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Step 2: Filter rows where recheck == 1 and drop missing values
df_filtered = df[df['recheck'] == 1].dropna(subset=['topic1'])

# Step 3: Count topic1 distribution
topic_counts = df_filtered['topic1'].value_counts()
total = topic_counts.sum()
percentages = topic_counts / total * 100
labels = topic_counts.index.tolist()
sizes = topic_counts.values.tolist()

# Step 4: Color setup
colors = plt.get_cmap('tab20c').colors  # Use a distinct colormap

# Step 5: Draw a donut chart
fig, ax = plt.subplots(figsize=(8, 8))
wedges, _ = ax.pie(sizes,
                   labels=None,
                   startangle=90,
                   counterclock=False,
                   colors=colors,
                   wedgeprops=dict(width=0.6))  # Donut width

# Add labels
for i, (wedge, label, pct) in enumerate(zip(wedges, labels, topic_counts)):
    theta = (wedge.theta2 + wedge.theta1) / 2
    angle_rad = np.deg2rad(theta)
    x = np.cos(angle_rad)
    y = np.sin(angle_rad)

    ax.text(0.7 * x, 0.7 * y, f"{pct}", ha='center', va='center',
                fontsize=16, fontname='Times New Roman')
    print(label)

# Add legend
ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5),
          fontsize=14, prop={'family': 'Times New Roman', 'size': 14})

# Styling
# ax.set_title("Topic1 Distribution (recheck == 1)", fontsize=14)
ax.axis('equal')

# Show plot
plt.tight_layout()
plt.show()
fig.savefig('fig/sunburst.pdf', format='pdf', dpi=600, bbox_inches='tight')




# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Step 1: Read the Excel file (update the path as needed)
# file_path = './vice.xlsx'  # Replace with your actual file path
# sheet_name = 'Sheet1'
# df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# # Step 2: Filter rows where recheck == 1 and drop missing values
# df_filtered = df[df['recheck'] == 1].dropna(subset=['topic1'])
#
# # Step 3: Count topic1 distribution
# topic_counts = df_filtered['topic1'].value_counts()
# total = topic_counts.sum()
# percentages = topic_counts / total * 100
# labels = topic_counts.index.tolist()
# sizes = topic_counts.values.tolist()
#
# # Step 4: Color setup
# colors = plt.get_cmap('tab20').colors  # Use a distinct colormap
#
# # Step 5: Draw a donut chart
# fig, ax = plt.subplots(figsize=(8, 8))
# wedges, _ = ax.pie(sizes,
#                    labels=None,
#                    startangle=90,
#                    counterclock=False,
#                    colors=colors,
#                    wedgeprops=dict(width=0.6))  # Donut width
#
# # Add percentage labels
# for i, (wedge, label, pct) in enumerate(zip(wedges, labels, percentages)):
#     theta = (wedge.theta2 + wedge.theta1) / 2
#     angle_rad = np.deg2rad(theta)
#     x = np.cos(angle_rad)
#     y = np.sin(angle_rad)
#
#     # Label placement: inside vs. outside
#     if pct < 4:
#         x1, y1 = 1.1 * x, 1.1 * y
#         x2, y2 = 1.3 * x, 1.1 * y
#         ha = 'left' if x2 > -0.2 else 'right'
#         x2 = -x2-0.15 if x2 > -0.2 else x2
#         ax.plot([x, x1], [y, y1], color='black', linewidth=1)
#         ax.plot([x1, x2], [y1, y2], color='black', linewidth=1)
#         ax.text(x2, y2, f"{label} ({pct:.1f}%)", ha=ha, va='center', fontsize=14, fontname='Times New Roman')
#     else:
#         if label=="Feature Requests Identification":
#             label = "Feature Requests\nIdentification"
#         ax.text(0.7 * x, 0.7 * y, f"{label}\n{pct:.1f}%", ha='center', va='center',
#                 fontsize=14, fontname='Times New Roman')
#         print(label)
#
# # Styling
# # ax.set_title("Topic1 Distribution (recheck == 1)", fontsize=14)
# ax.axis('equal')
#
# # Show plot
# plt.tight_layout()
# plt.show()
# fig.savefig('fig/sunburst.pdf', format='pdf', dpi=600, bbox_inches='tight')
#
