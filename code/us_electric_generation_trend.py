import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go

df = pd.read_csv("../data/7e._U.S._Electric_Generating_Capacity.csv", delimiter=',', skiprows=4)

relevant_data = df.iloc[3:][['remove', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']]

relevant_data = relevant_data.loc[:18,:].dropna()
relevant_data.columns = ['Source', '2018', '2019', '2020', '2021', '2022', '2023', '2024',
       '2025']
category_map = ['Natural gas', 'Coal', 'Nuclear', 'Wind', 'Solar', 'Battery storage']


consolidated_data = relevant_data.copy()
temp1 = {k:"" for k in category_map+['Others']}
for idx, row in relevant_data.iterrows():
    if row['Source'] in category_map:
        temp1[row['Source']] = row[1:]
    elif row['Source'] == 'Solar thermal' or row['Source'] == 'Solar photovoltaic':
        if type(temp1['Solar']) == str:
            temp1['Solar'] = row[1:]
        else:
            temp1['Solar'] += row[1:]
    else:
        if type(temp1['Others']) == str:
            temp1['Others'] = row[1:]
        else:
            temp1['Others'] += row[1:]

        

new_data = pd.DataFrame(temp1)
ordered_energy_data = new_data[['Others', 'Battery storage', 'Solar', 'Wind', 'Nuclear', 'Coal', 'Natural gas']]

plt.figure(figsize=(9, 5))

ax1 = plt.subplot(1, 2, 1)
ordered_energy_data.plot(kind='bar', stacked=True, ax=ax1, legend=False)
ax1.set_title('U.S. Electricity Generation by Source (2018-2025)', fontsize=10)
ax1.set_xlabel('Year')
ax1.set_ylabel('Generation (Gigawatts)')

normalized_energy = ordered_energy_data.div(ordered_energy_data.sum(axis=1), axis=0) * 100

ax2 = plt.subplot(1, 2, 2)
normalized_energy.plot(ax=ax2)
ax2.set_title('Share of Total Generation by Source (2018-2025)', fontsize=10)
ax2.set_xlabel('Year')
ax2.set_ylabel('Percentage (%)')
ax2.set_ylim(0, 50)
ax2.legend(title='Energy Source', loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

