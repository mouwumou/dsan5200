import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go

df = pd.read_csv("../data/MER_T01_01.csv")

descriptions = [
    "Total Fossil Fuels Production",
    "Total Renewable Energy Production",
    "Nuclear Electric Power Production",
    "Total Primary Energy Production"
]
filtered_data = df[(df['Description'].isin(descriptions)) & (~df['YYYYMM'].astype(str).str.endswith('13'))]




filtered_data['Year'] = pd.to_datetime(filtered_data['YYYYMM'], format='%Y%m', errors='coerce').dt.year
filtered_data = filtered_data.dropna(subset=['Year']) 
filtered_data = filtered_data.sort_values('Year')

anual_data = filtered_data.groupby(["Year","Description"]).agg({"Value":"sum"}).unstack()

rate_data = anual_data.pct_change().dropna() * 100
rate_data.drop(2024, inplace=True)

rate_fig = go.Figure()

rate_fig.add_trace(go.Scatter(
    x=rate_data.index,
    y=rate_data[('Value', 'Total Fossil Fuels Production')],
    mode='lines',
    name='Total Fossil Fuels Production',
    fillcolor='#AF8260'
))
rate_fig.add_trace(go.Scatter(
    x=rate_data.index,
    y=rate_data[('Value', 'Total Renewable Energy Production')],
    mode='lines',
    name='Total Renewable Energy Production',
    fillcolor='#7ABA78'
))
rate_fig.add_trace(go.Scatter(
    x=rate_data.index,
    y=rate_data[('Value', 'Nuclear Electric Power Production')],
    mode='lines',
    name='Nuclear Electric Power Production',
    fillcolor='#6DB9EF'
))

rate_fig.add_trace(go.Bar(
    x=rate_data.index,
    y=rate_data[('Value', 'Total Primary Energy Production')],
    name='Total Primary Energy Production',
))

rate_fig.update_layout(
    title='',
    xaxis_title='Date',
    yaxis_title='Increase Rate (%)',
    legend_title='Energy Types',
    xaxis_range=['2015', '2023']  
)

rate_fig.show()

