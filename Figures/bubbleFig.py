import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'

# Algorithm names, with a y-axis placeholder
algorithms_left  = ['DT', 'LR', 'MaxEnt', 'MNB', 'NB', 'RF', 'SVM']
algorithms_right = ['MLP', 'CNN', 'LSTM', 'TextRNN', 'BiLSTM', 'FastText', 'BERT']
algorithms = algorithms_left + [''] + algorithms_right  # '' is a y-axis placeholder

num_yaxis = len(algorithms_left)  # Index used for the y-axis column

# Years and their row positions (descending so it matches matplotlib's bottom-to-top plotting)
years = [2015,2016,2017,2018,2019,2020,2021,2022,2024,""]
year_pos = list(range(len(years)))  # 0,1,2,3,4,5,6

# Example bubble data
# (x position, y position, count, 'label', highlight?)
datas = [
    # DT (x=0)
    (0, 6.5, 2, '3,84', False),
    (0, 5.5, 2, '184\n155', False),
    (0, 4.5, 1, '157', False),
    (0, 3.5, 1, '167', False),
    (0, 2.5, 1, '46', False),
    (0, 1.5, 7, '170,113,\n109,135,\n133,45,\n156', False),
    (0, 0.5, 3, '64,134\n156', False),

    # LR (x=1)
    (1, 5.5, 3, '93,184\n155', False),
    (1, 4.5, 3, '5,92\n37', False),
    (1, 2.5, 1, '46', False),
    (1, 1.5, 2, '113', False),
    (1, 0.5, 1, '134\n156', False),  # From '16,39\\n48': '16' was removed (not mapped to new IDs)

    # MaxEnt (x=2)
    (2, 3.5, 1, '167', False),
    (2, 1.5, 1, '170', False),
    (2, 0.5, 1, '64', False),

    # MNB (x=3)
    (3, 5.5, 1, '93', False),
    (3, 4.5, 1, '92', False),
    (3, 1.5, 1, '113', False),

    # NB (x=4)
    (4, 6.5, 1, '3', False),
    (4, 5.5, 3, '184,180\n155,93', False),
    (4, 4.5, 4, '157,165\n37,166', False),
    (4, 3.5, 2, '121\n167', False),
    (4, 2.5, 3, '78,112\n46', False),
    (4, 1.5, 5, '170,109\n135,113', False),
    (4, 0.5, 4, '64,134\n150', False),

    # RF (x=5)
    (5, 8.5, 1, '1', False),
    (5, 6.5, 1, '3', False),
    (5, 5.5, 4, '93,184\n180,155', False),
    (5, 4.5, 2, '157\n92', False),
    (5, 1.5, 2, '109\n113', False),
    (5, 0.5, 1, '156', False),

    # SVM (x=6)
    (6, 6.5, 1, '77', False),
    (6, 5.5, 5, '93,184\n180,3\n119', False), #2021
    (6, 4.5, 4, '157,5\n37,92', False),
    (6, 3.5, 1, '121', False),
    (6, 2.5, 3, '78,112\n46', False),
    (6, 0.5, 1, '134', False),  # From '16,39': '16' was removed


    # MLP (x=7)
    (8, 5.5, 1, '93', False),
    (8, 4.5, 1, '92', False),

    # CNN (x=8)
    (9, 5.5, 3, '93,6\n74', False),
    (9, 4.5, 2, '157\n92', False),

    # LSTM (x=9)
    (10, 5.5, 1, '93', False),
    (10, 4.5, 1, '92', False),

    # TextRNN (x=10)
    (11, 5.5, 1, '93', False),
    (11, 4.5, 1, '92', False),

    # BiLSTM (x=11)
    (12, 5.5, 2, '153\n103', False),

    # FastText (x=12)
    (13, 6.5, 1, '84', False),
    (13, 4.5, 2, '157\n83', False),

    # BERT (x=13)
    (14, 7.5, 1, '77', False),  # ID 30 has no match and was removed, so it can be omitted

    # You can add more bubbles as needed
]



# Paper index/title → ML method mapping (notes)
# 91 khan2024miningMining: (MNB, LR, RF); deep learning (CNN, LSTM, BiLSTM)
# 1 abbas2024classification: Random Forest (ensemble learning)
# 3 izadi2022predicting: Feature engineering methods such as TF-IDF, with sentiment analysis assistance
# 74 al2021classification: Associative classification algorithms (CMAR, CBA)
# 116 nafees2021machine: SVM classifier

fig, ax = plt.subplots(figsize=(16, 8))

# ★ Shift all vertical grid lines right by 0.5
for xi in range(len(algorithms)):
    if xi == num_yaxis:
        ax.axvline(xi, color='black', linewidth=1.2, zorder=1)    # Thicker y-axis
    else:
        ax.axvline(xi, color='black', linewidth=1.2, linestyle='--', zorder=1)
# Horizontal grid lines remain at y - 0.5
for yi in range(len(years)):
    ax.axhline(yi - 0.5, color='black', linewidth=1.2, linestyle='--', zorder=1)

    # 1) Compute column totals
    col_total_counts = {}
    for x, y, count, label, highlight in datas:
        col_total_counts[x] = col_total_counts.get(x, 0) + count

    # 2) Add total paper count at the top of each column
    for xi, name in enumerate(algorithms):
        # Skip y-axis placeholder column
        if xi == num_yaxis:
            continue
        # Total (write 0 only if needed; omit if there are no bubbles)
        total = col_total_counts.get(xi, 0)
        # Top y position: max year row + ~0.8 to 1.0 (tweak if needed)
        ax.text(xi, len(years) - 0.5, str(total),
                ha='center', va='bottom', fontsize=10, color='black', zorder=10,)

# Bubble plot
for x, y, count, label, highlight in datas:
    # count=len(label.split(','))+1
    size = count * 470
    # if highlight:
    #     circle = plt.Circle((x, y), radius=(size/800)**0.5, edgecolor='cornflowerblue',
    #                         facecolor='aliceblue', lw=1, zorder=2)
    #     ax.add_patch(circle)
    #     plt.text(x, y, label, ha='center', va='center', fontsize=8, color='royalblue', weight='bold', zorder=3)
    # else:
    plt.scatter(x, y, s=size, edgecolor='black', facecolor='white', zorder=2)
    plt.text(x, y, label, ha='center', va='center', fontsize=9, color='black', zorder=3)

# X-axis labels (make the y-axis column blank)
xticks = list(range(len(algorithms)))
xticklabels = algorithms.copy()
xticklabels[num_yaxis] = ""  # Hide algorithm label on the y-axis column
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels, fontsize=13)


# # Put years on the y-axis (num_yaxis), shift up by 0.5, not bold
# for i, y in enumerate(year_pos):
#     ax.text(num_yaxis, y-0.5, years[i], ha='center', va='center', fontsize=16, zorder=5)


# # ★ Put years on the y-axis (num_yaxis), shift up by 0.5, not bold, with a white background
for i, y in enumerate(year_pos):
    ax.text(num_yaxis, y+0.5, years[i], ha='center', va='center', fontsize=13,
            zorder=5, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# # Write year labels on the y-axis column
# for i, y in enumerate(year_pos):
#     ax.text(num_yaxis, y, years[::-1][i], ha='center', va='center', fontsize=16, fontweight="bold", zorder=5)
# Upward arrow
arrow_x = num_yaxis
ax.annotate(
    '',
    xy=(arrow_x, len(years)-0.3), xycoords='data',
    xytext=(arrow_x, -0.5), textcoords='data',
    arrowprops=dict(arrowstyle="->", color="black", lw=1),
    annotation_clip=False
)
# x-axis
# Add a solid x-axis line at the bottom
ax.hlines(
    y=-0.5,                             # Bottom of y-axis; note years are in descending order
    xmin=-0.5, xmax=len(algorithms)-0.5,
    color='black', linewidth=2.2, zorder=10
)
# Overall settings
ax.set_xlim(-0.5, len(algorithms)-0.5)
ax.set_ylim(-0.5, len(years)-0.5)
ax.set_yticks([])
ax.set_xlabel('')
ax.set_ylabel('')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()
fig.savefig('fig/bubble.pdf', format='pdf', dpi=800, bbox_inches='tight')
