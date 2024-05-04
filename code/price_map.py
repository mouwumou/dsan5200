import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go

usa = gpd.read_file("./../data/cb_2018_us_state_5m/cb_2018_us_state_5m.shp")

fuelev = pd.read_csv("../data/Average_retail_price_of_electricity.csv", skiprows=5)

fuelev["State"] = fuelev["Unnamed: 0"].str.slice(3, 5)
melted_data = pd.melt(fuelev, id_vars=['State'], value_vars=[col for col in fuelev.columns if col.isdigit()], var_name='YearMonth', value_name='price')


plotly_map = usa.merge(melted_data, left_on='STUSPS', right_on='State')
plotly_map = plotly_map[~plotly_map["State"].isin(["AK", "HI"])]

fig = go.Figure()

color_scale = ["#fcffa4", "#bc3754", "#000004"]

unique_months = sorted(melted_data['YearMonth'].unique())
start_month = '202301'

for year in unique_months:
    fig.add_trace(
        go.Choropleth(
            locations=plotly_map['State'].unique(),
            z=plotly_map[plotly_map['YearMonth'] == year]['price'],  # or any other variable
            locationmode='USA-states',
            visible=(year == "202301"),
            colorscale=color_scale,
        )
    )

steps = []
for i, year in enumerate(unique_months):
    step = {
        'method': 'update',
        'args': [{'visible': [False] * len(unique_months)},  # Make all traces invisible
                 {'title': f'Showing data for year: {year}'}],  # Update the title
        'label': str(year)
    }
    step['args'][0]['visible'][i] = True
    steps.append(step)

sliders = [{
    'active': unique_months.index(start_month),
    'currentvalue': {'prefix': 'YearMonth: '},
    'steps': steps
}]

fig.update_layout(
    sliders=sliders,
    title="Electricity Retail Price by State Over Time",
    geo_scope='usa',
)

fig.show()