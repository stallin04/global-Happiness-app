#import plotly as plt
import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import seaborn as sns
import numpy as np


# Load your dataset
df = pd.read_excel('cleaned_global_happiness_with_iso.xlsx')  # Adjust path as needed

# Set the Streamlit page configuration for a cleaner look
st.set_page_config(page_title="Happiness Dashboard", page_icon="🌍", layout="wide")

# Title of the dashboard
st.title("Global Happiness Dashboard 🌍")

# Additional feature: Display info about the dashboard
st.markdown("""
### About this Dashboard
This dashboard allows you to explore the happiness scores of various countries around the world, visualize the trends over time, and analyze various factors like **GDP**, **Social Support**, **Generosity**, and **Freedom to make life choices**. Use the dropdown to select a country and explore its happiness data.

**Data Source**: The data is from the World Happiness Report.
""")

# Function to get the flag URL based on ISO code
def get_flag_url(iso_code):
    return f"https://flagpedia.net/data/flags/h80/{iso_code.lower()}.png"

# Create a sidebar for navigation (a great place to select the country)
country_dropdown = st.sidebar.selectbox(
    'Select a Country:',
    options=sorted(df['Country'].unique())
)

# Function to plot happiness trend and radar chart
def show_country_profile(country):
    country_df = df[df['Country'] == country].sort_values('Year')

    # Create two columns for a cleaner layout
    col1, col2 = st.columns([2, 1])

    # Line chart: happiness score over years
    with col1:
        st.subheader(f"Happiness Score Trend for {country}")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=country_df['Year'], y=country_df['Happiness score'],
            mode='lines+markers',
            name='Happiness Score'
        ))
        fig1.update_layout(
            title="",
            xaxis_title='Year',
            yaxis_title='Score',
            template='plotly_dark',
            plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        )
        st.plotly_chart(fig1)

    # Radar chart: latest year indicators
    with col1:
        latest = country_df[country_df['Year'] == country_df['Year'].max()]
        if not latest.empty:
            categories = ['GDP per capita', 'Social support', 'Healthy life expectancy',
                          'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']
            values = latest[categories].values.flatten().tolist()
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=country
            ))
            fig2.update_layout(
                title=f"Indicator Profile for {country} ({latest['Year'].values[0]})",
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=False,
                template='plotly_dark',
                plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
            )
            st.plotly_chart(fig2)

    # Get the flag URL based on the ISO code and display it
    iso_code = latest['ISO_Code'].values[0]  # Get the ISO code
    flag_url = get_flag_url(iso_code)  # Fetch the flag URL based on ISO code
    with col2:
        st.image(flag_url, width=150)  # Display the flag image

    # Display the country's key stats
    with col2:
        st.markdown(f"### Key Stats for {country}")
        st.write(f"**Happiness Score**: {latest['Happiness score'].values[0]}")
        st.write(f"**GDP per capita**: {latest['GDP per capita'].values[0]}")
        st.write(f"**Social Support**: {latest['Social support'].values[0]}")

# Display the country profile when a country is selected
show_country_profile(country_dropdown)

# Additional Visualizations:
## Global Happiness Distribution (Choropleth map)
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_excel('cleaned_global_happiness_with_iso.xlsx')  # Adjust path as needed

# Ensure 'Happiness score' is numeric and handle missing values
df['Happiness score'] = pd.to_numeric(df['Happiness score'], errors='coerce')
df = df.dropna(subset=['Happiness score', 'Country'])

# Get the latest year data
latest_year = df['Year'].max()
df_latest = df[df['Year'] == latest_year]

# Subheader for Global Happiness Distribution
st.subheader("Global Happiness Distribution (Selected Country Highlighted)")

# Filter data for the selected country
selected_country_df = df_latest[df_latest['Country'] == country_dropdown]

# Create choropleth map
fig_map = px.choropleth(
    df_latest,
    locations="ISO_Code",
    color="Happiness score",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Plasma,
    projection="natural earth"
)

# Add a marker layer for the selected country to highlight it
if not selected_country_df.empty:
    fig_map.add_scattergeo(
        locations=selected_country_df['ISO_Code'],
        locationmode='ISO-3',
        text=selected_country_df['Country'],
        marker=dict(size=15, color='red'),
        name=f"Selected: {country_dropdown}"
    )

# Update the map layout
fig_map.update_layout(
    title=f"Happiness Scores by Country — Highlight: {country_dropdown}",
    geo=dict(
        showcountries=True,
        projection_type='natural earth'
    )
)

# Display the map
st.plotly_chart(fig_map)

## Correlation Heatmap (Plotly)
st.subheader("Correlation Heatmap of Happiness Indicators")
corr_df = df[['Happiness score', 'GDP per capita', 'Social support', 'Healthy life expectancy',
              'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']].corr()

# Create Plotly heatmap instead of Matplotlib
fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr_df.values,
    x=corr_df.columns,
    y=corr_df.columns,
    colorscale='Viridis',
    colorbar=dict(title='Correlation')
))
fig_heatmap.update_layout(title='Correlation Heatmap')
st.plotly_chart(fig_heatmap)

## Top 10 Happiest Countries Bar Chart
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel('cleaned_global_happiness_with_iso.xlsx')
st.subheader("Top 10 Happiest Countries")

df['Happiness score'] = pd.to_numeric(df['Happiness score'], errors='coerce')
df = df.dropna(subset=['Happiness score', 'Country'])

# Get the latest year if there are multiple years
latest_year = df['Year'].max()
df_latest = df[df['Year'] == latest_year]

top_10 = df_latest.nlargest(10, 'Happiness score').sort_values('Happiness score', ascending=True)

fig_bar = px.bar(
    top_10,
    x='Happiness score',
    y='Country',
    orientation='h',
    title="Top 10 Happiest Countries",
    color_discrete_sequence=['green'] * 10
)

fig_bar.update_layout(
    xaxis_title='Happiness Score',
    yaxis_title='Country',
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(categoryorder='total ascending')
)

st.plotly_chart(fig_bar)


## Happiness vs GDP Scatter Plot
st.subheader("Happiness vs GDP per Capita")
fig_scatter = px.scatter(df, x='GDP per capita', y='Happiness score', color='Country', hover_name='Country',
                         title="Happiness vs GDP per Capita", color_continuous_scale='Viridis')
st.plotly_chart(fig_scatter)




