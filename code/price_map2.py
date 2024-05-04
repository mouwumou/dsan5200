import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

usa = gpd.read_file("./../data/cb_2018_us_state_5m/cb_2018_us_state_5m.shp")

fuelev = pd.read_csv("../data/Average_retail_price_of_electricity.csv", skiprows=5)

fuelev["State"] = fuelev["Unnamed: 0"].str.slice(3, 5)
melted_data = pd.melt(fuelev, id_vars=['State'], value_vars=[col for col in fuelev.columns if col.isdigit()], var_name='YearMonth', value_name='price')


plotly_map = usa.merge(melted_data, left_on='STUSPS', right_on='State')
plotly_map = plotly_map[~plotly_map["State"].isin(["AK", "HI"])]


df = pd.read_csv("../data/MER_T01_01.csv")

descriptions = [
    "Total Fossil Fuels Production",
    "Total Renewable Energy Production",
    "Nuclear Electric Power Production"
]
filtered_data = df[(df['Description'].isin(descriptions)) & (~df['YYYYMM'].astype(str).str.endswith('13'))]

pivot_data = filtered_data.pivot_table(index='YYYYMM', columns='Description', values='Value', aggfunc='sum')

pivot_data.reset_index(inplace=True)

pivot_data.columns = ['YearMonth', 'Nuclear', 'Fossil Fuels', 'Renewable']

pivot_data['YearMonth'] = pivot_data['YearMonth'].astype(str)

# pivot_data[pivot_data['YearMonth'].isin(unique_months)].reset_index(drop=True)





fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Electricity Prices", "Electirc Produced Sources", "Electric Produced Sources Over Last 6 Months"),
    specs=[[{"type": "choropleth", "colspan": 2}, None],
           [{"type": "bar"}, {"type": "scatter"}]],
    column_widths=[0.5, 0.5],
    row_heights=[0.66, 0.34]
)

color_scale = ["#fcffa4", "#bc3754", "#000004"]
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
line_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

unique_months = sorted(melted_data['YearMonth'].unique())
start_ym = '202301'
max_y = pivot_data[['Nuclear', 'Fossil Fuels', 'Renewable']].max().max()
min_price = plotly_map['price'].min()
max_price = plotly_map['price'].max()


def get_last_6_months_data(month, df):
    month_index = df[df['YearMonth'] == month].index[0]
    start_index = max(0, month_index - 5)
    return df.iloc[start_index:month_index+1]


for ym in unique_months:
    visible = (ym == start_ym)
    fig.add_trace(
        go.Choropleth(
            locations=plotly_map['State'].unique(),
            z=plotly_map[plotly_map['YearMonth'] == ym]['price'],  # or any other variable
            locationmode='USA-states',
            visible=visible,
            zmin=min_price,
            zmax=max_price,
            colorscale=color_scale,
        ),
        row=1, col=1
    )

    if ym in pivot_data['YearMonth'].values:
        month_data = pivot_data[pivot_data['YearMonth'] == ym]

        fig.add_trace(
            go.Bar(
                x=['Nuclear', 'Fossil Fuels', 'Renewable'],
                y=[month_data['Nuclear'].values[0], month_data['Fossil Fuels'].values[0], month_data['Renewable'].values[0]],
                visible=visible,
                marker_color=bar_colors,
                showlegend=False
            ),
            row=2, col=1
        )

        fig.update_yaxes(range=[0, max_y], row=2, col=1)

    last_6_months_data = get_last_6_months_data(ym, pivot_data)
    for energy_type, color in zip(['Nuclear', 'Fossil Fuels', 'Renewable'], line_colors):
        fig.add_trace(
            go.Scatter(
                x=last_6_months_data['YearMonth'],
                y=last_6_months_data[energy_type],
                mode='lines+markers',
                name=energy_type,
                line=dict(color=color),
                visible=visible,
                showlegend=False
            ),
            row=2, col=2
        )

        fig.update_yaxes(range=[0, max_y], row=2, col=2)

steps = []
for i, ym in enumerate(unique_months):
    step_visible = [False] * (len(unique_months) * 5)  # 5 traces per month (1 map, 1 bar, 3 lines)
    for j in range(5):
        step_visible[i * 5 + j] = True
    
    steps.append({
        'method': 'update',
        'args': [{'visible': step_visible}],
        'label': ym
    })


sliders = [{
    'active': unique_months.index(start_ym),
    'currentvalue': {'prefix': 'YearMonth: '},
    'steps': steps
}]

fig.update_layout(
    width=880, 
    height=800,
    margin=dict(l=20, r=20, t=50, b=20),
    sliders=sliders,
    title="Electricity Retail Price by State Over Time",
    geo_scope='usa',
)

fig.show()