import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import plotly.graph_objects as go

df = pd.read_csv("../data/MER_T01_01.csv")

descriptions = [
    "Total Fossil Fuels Consumption",
    "Total Renewable Energy Consumption",
    "Nuclear Electric Power Consumption"
]
filtered_data = df[(df['Description'].isin(descriptions)) & (~df['YYYYMM'].astype(str).str.endswith('13'))]

filtered_data['Date'] = pd.to_datetime(filtered_data['YYYYMM'], format='%Y%m', errors='coerce')
filtered_data = filtered_data.dropna(subset=['Date'])  # Drop rows where date conversion failed
filtered_data = filtered_data.sort_values('Date')

pivot_data = filtered_data.pivot_table(index='Date', columns='Description', values='Value', aggfunc='sum')

pivot_data 


fig = go.Figure()

fig.add_trace(go.Scatter(
    x=pivot_data.index,
    y=pivot_data['Total Fossil Fuels Consumption'],
    mode='lines',
    stackgroup='one', 
    name='Total Fossil Fuels Consumption',
    fillcolor='#AF8260'
))
fig.add_trace(go.Scatter(
    x=pivot_data.index,
    y=pivot_data['Total Renewable Energy Consumption'],
    mode='lines',
    stackgroup='one',
    name='Total Renewable Energy Consumption',
    fillcolor='#7ABA78'
))
fig.add_trace(go.Scatter(
    x=pivot_data.index,
    y=pivot_data['Nuclear Electric Power Consumption'],
    mode='lines',
    stackgroup='one',
    name='Nuclear Electric Power Consumption',
    fillcolor='#6DB9EF'
))

fig.update_layout(
    title='Interactive Energy Consumption Stack Graph (2023 Focus)',
    xaxis_title='Date',
    yaxis_title='Energy Consumption (Quadrillion Btu)',
    legend_title='Energy Types',
    xaxis_range=['2023-01-01', '2023-12-31']  
)

fig.show()
