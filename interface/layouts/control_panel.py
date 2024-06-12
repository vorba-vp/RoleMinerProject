from dash import dcc, html

control_panel_layout = html.Div(
    children=[
        html.H1("Role Mining Tool"),
        html.Div(
            children=[
                dcc.Dropdown(
                    id="dataset-dropdown",
                    options=[
                        {"label": "Simple Dataset", "value": "simple_dataset"},
                        {"label": "Identity Matrix", "value": "identity_matrix"},
                    ],
                    placeholder="Select an option",
                    style={"width": "200px"},
                ),
                html.Button(
                    "Show UPA", id="show-upa-button", style={"margin-left": "30px"}
                ),
            ],
            style={"display": "flex"},
        ),
        html.Div(id="warning-message", style={"color": "red", "margin-top": "10px"}),
    ],
    style={"height": "15vh"},
)
