import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go


raw = pd.read_excel('../data/Region_TEX.xlsx', sheet_name="Daily Charts", header=1)

raw = raw[raw["Local date"] > "2023-05-1"]
raw = raw[raw["Local date"] < "2024-04-1"]

daily = raw[["Local date", "Demand", "Net generation", "Coal", "Natural gas", "Petroleum", "Hydro", "Solar", "Wind", "Other"]].dropna()

daily.to_csv('../data/daily.csv', index=False)

daily["all other"] = daily["Coal"] + daily["Natural gas"] + daily["Petroleum"] + daily["Other"] + daily["Hydro"]

data = daily.copy()
data['Local date'] = pd.to_datetime(data['Local date'])
generation_types_columns = ['all other', 'Wind', 'Solar']
data['YearMonth'] = data['Local date'].dt.to_period('M')
data = data.set_index('Local date')
monthly_data = data.groupby('YearMonth').sum()
monthly_generation_data = monthly_data[generation_types_columns]
monthly_generation_data.index = monthly_generation_data.index.to_timestamp()

plt.figure(figsize=(9, 5))

ax1 = plt.subplot(1, 2, 1)
ax1.stackplot(monthly_generation_data.index, monthly_generation_data.T, labels=generation_types_columns, colors=["gray", "lightblue", "orange"], alpha=0.8)
# plt.legend(loc='upper left')
ax1.set_xlim([pd.Timestamp('2023-05-01'), pd.Timestamp('2024-02-28')])
ax1.set_title('Monthly Generation Trend by Source')
ax1.set_xlabel('Month')
ax1.set_ylabel('Generation Monthly (MWh)')
ax1.grid(axis="x")
ax1.set_ylim([0, 60000000])
ax1.set_xticks(['2023-05','2023-08', '2023-11', '2024-02'], ["Spring", "Summer", "Fall", "Winter"])
ax1.legend(frameon=False, loc='upper right', labelcolor = "linecolor", )


ax2 = plt.subplot(1, 2, 2)
total_generation = data[generation_types_columns].sum()
total_generation['Other'] = total_generation.sum() - total_generation['Solar'] - total_generation['Wind']

pie_chart_data = total_generation[['Solar', 'Wind', 'Other']]
ax2.pie(pie_chart_data, labels=pie_chart_data.index, autopct='%1.1f%%', startangle=0, colors=['orange', 'lightblue', 'gray'])
ax2.set_title('Percentage of Solar, Wind, and Other Energy Sources')
plt.tight_layout()
plt.show()