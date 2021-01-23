import pandas as pd
import plotly.graph_objects as go
from math import floor
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
server = app.server
app.title = "Blood Alcohol Level"

test_df = pd.read_excel("testdata.xlsx")


time = [f"{i}:00" for i in range(12)]
z = [i**2 for i in range(12)]

app.layout = html.Div(
    [
        html.Div([
            html.H1("Blood Alcohol Predictor"),

            html.Label("Select your sex", style={"margin": "5px"}),
            html.Br(),

            dcc.Dropdown(
                id="sex", options=[
                    {
                        "label": "Male", "value": "Male"}, {
                        "label": "Female", "value": "Female"},

                ], multi=False, value="ALL", style={
                    "background": "black"}),
            html.Br(),
            html.Label("Select your age", style={"margin": "5px"}, id="AGE"),
            dcc.Slider(
                id="age",
                min=18,
                max=60,
                step=1,
                value=18,
                marks={2 * i: str(2 * i) for i in range(36)},


            ),

            html.Br(),
            html.Label("Height", style={"margin": "5px"}, id="HEIGHT"),
            dcc.Slider(
                id="height",
                min=140,
                max=230,
                step=1,
                value=170,
                marks={10 * i: str(10 * i) for i in range(24)},
            ),
            html.Br(),
            html.Label("Weight", style={"margin": "5px"}, id="WEIGHT"),
            dcc.Slider(
                id="weight",
                min=20,
                max=200,
                step=1,
                value=70,
                marks={10 * i: str(10 * i) for i in range(21)},
            ),
        ], id="container"),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([

            html.Div(
                html.H1("Enter Drink"), style={'width': '32%', 'display': 'inline-block'}),

            html.Div(
                html.H1("Enter Volume of that drink in mL"), style={'width': '32%', 'display': 'inline-block'}),
            html.Div(
                html.H1("Enter the time you drunk it"),
                style={'width': '32%', 'display': 'inline-block'}),



        ]),

        html.Div([

            html.Div(
                dcc.Input(
                    id="drink_inp",
                    placeholder="Enter Drink"
                ), style={'width': '32%', 'display': 'inline-block', "text-align": "center", }),

            html.Div(
                dcc.Input(
                    id="volume_inp",
                    placeholder="Enter Enter Volume (mL)"
                ), style={'width': '32%', 'display': 'inline-block', "text-align": "center"}),
            html.Div(
                dcc.Input(
                    id="time_inp",
                    placeholder="Enter Time"
                ),
                style={'width': '32%', 'display': 'inline-block', "text-align": "center"}),



        ]),


        html.Br(),
        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        html.Br(),
        html.Div(id='output_div'),

        html.Br(),
        dash_table.DataTable(
            id='table',
            columns=[

                {
                    'name': "Drink",
                    'id': "Drink",
                    'deletable': False,
                    'renamable': False
                },

                {
                    'name': "Volume (mL)",
                    'id': "Volume (mL)",
                    'deletable': False,
                    'renamable': False
                },
                {
                    'name': "Time",
                    'id': "Time",
                    'deletable': False,
                    'renamable': False
                }



            ],
            data=test_df.to_dict("records"),

            editable=False,
            row_deletable=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'textAlign': 'left',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Region'},
                    'textAlign': 'left'
                }]



        ),








        dcc.Graph(
            id="graph", figure={

            },

        ),



    ], id="data",

)


@app.callback(
    Output("table", "data"),
    Input('editing-rows-button', 'n_clicks'),
    State(component_id="drink_inp", component_property="value"),
    State(component_id="volume_inp", component_property="value"),
    State(component_id="time_inp", component_property="value"),
    State(component_id="table", component_property="data")

)
def add(c, d, v, t, og_data):
    if c > 0:
        global test_df
        ss = pd.DataFrame(og_data, columns=["Drink", "Volume (mL)", "Time"])
        test_df = ss

        test_df.loc[-1] = [d, v, t]
        test_df.index = test_df.index + 1
        test_df = test_df.sort_index()
        data = test_df.to_dict("records")
        print(test_df)
        return data


@app.callback(
    [Output(component_id="AGE", component_property="children"),
     Output(component_id="HEIGHT", component_property="children"),
     Output(component_id="WEIGHT", component_property="children"),
     Output(component_id="graph", component_property="figure")

     ],
    [Input(component_id="age", component_property="value"),
     Input(component_id="height", component_property="value"),
     Input(component_id="weight", component_property="value"),


     ]

)
def update(age, height, weight):
    age_txt = f"Age selected: {age} years"

    ft = 0.0328 * height
    number_dec = str(ft - int(ft))[1:]

    height_ft_inch = f"{floor(ft)}ft {round(float(number_dec)*12,1)}in"

    height_txt = f"Height selected: {height} cm == {height_ft_inch}"
    weight_txt = f"Weight: {weight}kg"

    figure = go.Figure(data=go.Scatter(
        x=time,
        y=z,

    ))

    figure.update_traces(line_color="white", textfont_color="white", selector=dict(type='scatter'), marker_colorbar_tickcolor="white"
                         )

    figure.update_xaxes(showgrid=False, zeroline=False, tickcolor='white',
                        tickfont=dict(color='white'))

    figure.update_yaxes(showgrid=False, zeroline=False, tickcolor='white',
                        tickfont=dict(color='white'))

    figure.update_layout(
        plot_bgcolor="#1f1f1f",
        paper_bgcolor="#2c2c2c",

    )

    return age_txt, height_txt, weight_txt, figure


if __name__ == "__main__":
    app.run_server(debug=True)
