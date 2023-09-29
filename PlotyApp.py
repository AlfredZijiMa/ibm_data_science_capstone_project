# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})
# Create a dash application
app = dash.Dash(__name__)


app.layout = html.Div(children=[ html.H1('Airline Performance Dashboard',
                                         style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                 html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010',
                                                                     type='number', style={'height':'50px', 'font-size': 35}),],
                                          style={'font-size': 40}),

                                 # Task 1 Add a dropdown list to enable Launch Site selection
                                 dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                  {'label': 'All Sites', 'value': 'All Sites'},
                                                  {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                  {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                  {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                  {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                              ],
                                              placeholder='Select a Launch Site Here',
                                              value='All Sites',
                                              searchable=True
                                              ),

                                 html.Br(),
                                 html.Br(),


                                 # Task 2 Add a pie chart to show the total successful launches count for all sites

                                 html.Div(dcc.Graph(id='success-pie-chart')),
                                 html.Br(),

                                 html.P("Payload range (Kg):"),

                                 # Task 3 Add a slider to select payload range

                                 dcc.RangeSlider(id='payload-slider',
                                                 min=0,
                                                 max=10000,
                                                 step=1000,
                                                 marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},
                                                 value=[min_payload, max_payload]),


                                 # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                 html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                 html.Div(dcc.Graph(id='line-plot')),
                                 ])


# # add callback decorator
# @app.callback( Output(component_id='line-plot', component_property='figure'),
#                Input(component_id='input-year', component_property='value'))

# Taks 2: app call back
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select 2019 data
    df =  airline_data[airline_data['Year']==int(entered_year)]

    # Group the data by Month and compute average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# Task 3 pie chart methods
def get_pie_chart(launch_site):
    if launch_site == 'All Sites':
        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].mean(),
                     names=spacex_df.groupby('Launch Site')['Launch Site'].first(),
                     title='Total Success Launches by Site')
    else:
        fig = px.pie(values=spacex_df[spacex_df['Launch Site']==str(launch_site)]['class'].value_counts(normalize=True),
                     names=spacex_df['class'].unique(),
                     title='Total Success Launches for Site {}'.format(launch_site))
    return(fig)

# Task 4 payload_chart
def get_payload_chart(launch_site, payload_mass):
    if launch_site == 'All Sites':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])],
                         x="Payload Mass (kg)",
                         y="class",
                         color="Booster Version Category",
                         hover_data=['Launch Site'],
                         title='Correlation Between Payload and Success for All Sites')
    else:
        df = spacex_df[spacex_df['Launch Site']==str(launch_site)]
        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])],
                         x="Payload Mass (kg)",
                         y="class",
                         color="Booster Version Category",
                         hover_data=['Launch Site'],
                         title='Correlation Between Payload and Success for Site {}'.format(launch_site))
    return(fig)

# Run the app
if __name__ == '__main__':
    app.run_server()