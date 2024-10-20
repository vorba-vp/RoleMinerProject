import dash_daq as daq
from dash import dcc, html

control_panel_layout = html.Div(
    children=[
        html.H1("Role Mining Tool"),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Span(
                            id="control-panel-label-1",
                            children="Algorithms Inputs",
                            style={
                                "margin-left": "30px",
                                "margin-right": "5px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                        dcc.Dropdown(
                            id="dataset-dropdown",
                            options=[
                                {"label": "Simple Dataset", "value": "simple_dataset"},
                                {
                                    "label": "Identity Matrix",
                                    "value": "identity_matrix",
                                },
                                {"label": "Healthcare Dataset", "value": "healthcare"},
                                {
                                    "label": "Americas Large Dataset",
                                    "value": "americas_large",
                                },
                                {
                                    "label": "Americas Small Dataset",
                                    "value": "americas_small",
                                },
                                {"label": "APJ Dataset", "value": "apj"},
                                {"label": "Customer Dataset", "value": "customer"},
                                {"label": "Domino Dataset", "value": "domino"},
                                {"label": "EMEA Dataset", "value": "emea"},
                                {"label": "Firewall 1 Dataset", "value": "firewall-1"},
                                {"label": "Firewall 2 Dataset", "value": "firewall-2"},
                            ],
                            placeholder="Choose a dataset",
                            style={"width": "200px"},
                        ),
                        html.Span(
                            id="d-factor-label",
                            children="RMP \u03b4 -Factor:",
                            style={
                                "margin-left": "30px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                        daq.NumericInput(
                            id="d-factor-input",
                            value=0,
                            style={"margin-left": "5px"},
                        ),
                    ],
                    style={"display": "flex", "flex-direction": "row"},
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Show UPA",
                            id="show-upa-button",
                            style={"margin-left": "30px"},
                        ),
                        html.Button(
                            "Show FastMiner Result",
                            id="show-fm-button",
                            style={"margin-left": "30px"},
                        ),
                        html.Button(
                            "Show Basic RMP Results",
                            id="show-brmp-button",
                            style={"margin-left": "30px"},
                        ),
                        html.Br(),
                        html.Button(
                            "Clear",
                            id="clear-button",
                            style={"margin-left": "30px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "margin-top": "10px",
                    },
                ),
            ],
            style={"display": "flex", "flex-direction": "column"},
        ),
        html.Div(id="warning-message", style={"color": "red", "margin-top": "10px"}),
    ],
    style={"height": "15vh"},
)
