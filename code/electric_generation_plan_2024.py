import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go




df = pd.read_excel("../data/december_generator2023.xlsx", skiprows=2, sheet_name="Planned")
df = df[df["Planned Operation Year"] == 2024]
df = df[["Planned Operation Month", "Energy Source Code", "Nameplate Capacity (MW)"]]
df["Source"] = df["Energy Source Code"].apply(lambda x: "Solar" if x == "SUN" else "Wind" if x == "WND" else "Natural Gas" if x == "NG" else "Battery Storage" if x == "MWH" else "Other")
df = df[["Planned Operation Month", "Nameplate Capacity (MW)", "Source"]]
df["Nameplate Capacity (GW)"] = df["Nameplate Capacity (MW)"] / 1000
import matplotlib.pyplot as plt
data = df
# Convert 'Planned Operation Month' to integer if necessary
data['Planned Operation Month'] = data['Planned Operation Month'].astype(int)

# Create a pivot table to aggregate the nameplate capacity by month and source
pivot_data = data.pivot_table(
    values='Nameplate Capacity (GW)', 
    index='Planned Operation Month', 
    columns='Source', 
    aggfunc='sum',
    fill_value=0
)

# Sort the columns in the pivot table so that the largest total capacities are at the bottom of the stack
sorted_sources = pivot_data.sum().sort_values(ascending=False).index

# Replot with the sorted order
pivot_data_sorted = pivot_data[sorted_sources]


source_capacity = data.groupby('Source')['Nameplate Capacity (GW)'].sum().sort_values(ascending=False)

# Generate both plots in one figure with a consistent color palette, sharing the legend

# Get unique colors for each source
colors = plt.cm.tab20(range(len(source_capacity)))

# Create figure and axes for the subplots
fig, axs = plt.subplots(1, 2, figsize=(11, 3),)

# Stacked bar plot
pivot_data_sorted.plot(kind='bar', stacked=True, color=colors, ax=axs[0])
axs[0].set_title('US planned electric generation addiction by source(2024)', fontsize=16, fontweight='bold', loc = 'left')
axs[0].set_xlabel('Month')
axs[0].set_ylabel('Nameplate Capacity (GW)')
axs[0].tick_params(axis='x', rotation=0)
axs[0].legend([])

wedges, texts, autotexts = axs[1].pie(
    source_capacity, 
    labels=source_capacity.index, 
    autopct='%1.1f%%', 
    startangle=180, 
    colors=colors, 
    wedgeprops=dict(width=0.55)
)

# Update autopct and label text colors to match the slices
for text, autotext, color in zip(texts, autotexts, colors):
    text.set_color(color)
    autotext.set_color("w")
    
axs[1].set_facecolor('#D3D3D3')
# axs[1].set_title('Total Nameplate Capacity by Source')
axs[1].axis('equal')  # Draw as a circle

total_capacity = source_capacity.sum()
axs[1].text(0, 0, f'Total\n{total_capacity.round(2)} GW\nin 2024', ha='center', va='center', fontsize=12, color='black')


# Draw the pie chart as a circle
axs[1].axis('equal')

plt.subplots_adjust(right=0.8)

plt.show()
