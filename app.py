# Deployment link:

# Link to dataset: https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load and clean data from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals'
tables = pd.read_html(url)
world_cup_finals = tables[3]  # Table with match results

# Consolidate Germany data
world_cup_finals['Winners'] = world_cup_finals['Winners'].replace(['Germany FR', 'West Germany'], 'Germany')
world_cup_finals['Runners-up'] = world_cup_finals['Runners-up'].replace(['Germany FR', 'West Germany'], 'Germany')

# Prepare wins per country data
win_counts = world_cup_finals['Winners'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={"textAlign": "center"}),

    dcc.Graph(id='choropleth-map',
              figure=px.choropleth(
                  win_counts,
                  locations="Country",
                  locationmode="country names",
                  color="Wins",
                  color_continuous_scale="Blues",
                  title="Total World Cup Wins by Country"
              )),

    html.Br(),
    html.H2("Select a Country to View Win Count"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in win_counts['Country']],
        placeholder="Select a country"
    ),
    html.Div(id='country-output', style={'marginTop': 20}),

    html.Br(),
    html.H2("Select a Year to View Winner and Runner-up"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in world_cup_finals['Year']],
        placeholder="Select a year"
    ),
    html.Div(id='year-output', style={'marginTop': 20})
])

# Country callback
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def display_country_wins(selected_country):
    if selected_country is None:
        return ""
    wins = win_counts[win_counts['Country'] == selected_country]['Wins'].values[0]
    return f"{selected_country} has won the FIFA World Cup {wins} time(s)."

# Year callback
@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def display_year_results(selected_year):
    if selected_year is None:
        return ""
    row = world_cup_finals[world_cup_finals['Year'] == selected_year].iloc[0]
    return f"In {selected_year}, the winner was {row['Winners']} and the runner-up was {row['Runners-up']}."

# Run server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)

