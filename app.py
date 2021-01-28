import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

# For Plotly Graphs and Charts
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Style for Scatterfig (Crime Pie Chart)
style = "mapbox://styles/kshizi/ckkgih80b043k17p0krxnbssu"
px.set_mapbox_access_token(open("data/.mapbox_token").read())


# Data Frame
df = pd.read_csv('data/Raleigh_Police_Incidents.csv')

# Data Wrangling
list_in_dist = df['district']
count = list_in_dist.value_counts(dropna=True)
count_tolist = list(count)
index_tolist = count.index.tolist()

# Wrangled Data Passed into Pie Chart
labels = index_tolist
values = count_tolist


# Crime Pie Chart Figure
fig = go.Figure(data=[go.Pie(labels=labels,
                             values=values,
                             textinfo='label+percent',
                             insidetextorientation='radial'
                             )
                      ]
                )
fig_update = fig.update_layout(
    title_text="Crime Percentage Per District in Raleigh, NC")


# Crime Map 1
scatterfig = px.scatter_mapbox(df, lat="Y", lon="X", color="district", size="reported_month",
                               color_continuous_scale=px.colors.cyclical.IceFire, size_max=12, zoom=10)

scatterfig.update_mapboxes(style=style)


# Crime Table
ccategory_index = ((df['crime_category']).value_counts(dropna=True)).index.tolist()
ccode_index = ((df['crime_code']).value_counts(dropna=True)).index.tolist()

fig_table = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                                     cells=dict(values=[ccode_index, ccategory_index]))
                            ])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

app.layout = dbc.Container(html.Div(
    # Header: includes logo, title, and clickable links
    # Main Title
    [
        dbc.Row(dbc.Col(style={'padding': 30})),
        dbc.Row(
            [
                dbc.Col(html.Div(html.Img(src='static/Kola Logo w.png',
                                          height='35',
                                          width='true'))),
                dbc.Col(html.Div(html.P("Raleigh NC Crime Incidents"),
                                 style={'color': 'white',
                                        'fontSize': 29,
                                        'text-align': 'center'
                                        }
                                 )
                        ),

                # Header: Clickable Images
                dbc.Col(html.Div([
                    html.A([
                        html.Img(
                            src='static/Email_Black.png',
                            style={
                                'height': '12%',
                                'width': '12%',
                                'float': 'right',
                                'position': 'relative',
                                'padding-top': 0,
                                'padding-right': 0,
                                'left': 0,
                                'bottom': 0})
                    ], href='mailto:carlfoshizi@gmail.com'),
                    html.A([
                        html.Img(
                            src='static/LinkedIn_Black.png',
                            style={
                                'height': '12%',
                                'width': '12%',
                                'float': 'right',
                                'position': 'relative',
                                'padding-top': 0,
                                'padding-right': 0,
                                'right': 20,
                                'bottom': 0})
                    ], href='https://www.linkedin.com/in/kola-ladipo/'),
                    html.A([
                        html.Img(
                            src='static/Github_Black.png',
                            style={
                                'height': '12%',
                                'width': '12%',
                                'float': 'right',
                                'position': 'relative',
                                'padding-top': 0,
                                'padding-right': 0,
                                'right': 40,
                                'bottom': 0})
                    ], href='https://github.com/carlshizi?tab=repositories/')
                ]))
            ]
        ),


        # Subtitle
        dbc.Row(dbc.Col(html.Div(html.P("National Incident Based Reporting System (NIBRS)",
                                        style={'fontSize': 18,
                                               'text-align': 'center',
                                               }
                                        )
                                 )
                        )
                ),


        # Spacing
        dbc.Row(dbc.Col(html.Div(style={'padding': 20}))),


        # Info and Table
        dbc.Row(dbc.Col(html.Div(
            html.Div(
                [
                    dbc.Card(
                        dbc.CardBody("NIBRS establishes a new "
                                     "baseline that more precisely "
                                     "captures reported crime in a community",),
                        className="mb-3"
                    )
                ]
            )
        ))),
        #
        dbc.Row(dbc.Col(html.Div(style={'padding': 25}))),


        # MAIN INTERACTIVE CHART!!!
        dbc.Row(dbc.Col(dcc.Graph(
            figure=scatterfig
        ))),

        #
        dbc.Row(dbc.Col(html.Div(style={'padding': 20}))),


        # Two Plotly Graphs
        dbc.Row(
            [

                # Plotly Graph 1
                dbc.Col(dcc.Graph(
                    id='Crime Percentage Per District in Raleigh, NC',
                    figure=fig
                )),

                # Plotly Graph 2
                dbc.Col(dcc.Graph(
                    id='',
                    figure=fig_table
                )),
            ]
        )
    ]
), fluid=False

)

if __name__ == "__main__":
    app.run_server()
