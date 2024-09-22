from dash import dash_table, dcc, html


def get_rmp_results_layout():
    return html.Div(
        children=[
            html.H2("RMP Result"),
            dcc.Loading(
                id="loading-rmp",
                type="default",
                children=[
                    # PA Matrix (Roles and Permissions)
                    html.Div(
                        [
                            html.H3("PA Matrix (Roles to Permissions)"),
                            dash_table.DataTable(
                                id="pa-matrix-table",
                                columns=[],  # Will be populated dynamically
                                data=[],  # Will be populated dynamically
                                style_cell={"textAlign": "left"},
                                sort_action="native",
                                page_size=20,
                                style_data_conditional=[
                                    {
                                        "if": {
                                            "filter_query": '{Role} = ""'
                                        },  # Apply to empty rows
                                        "backgroundColor": "#f9f9f9",
                                        "color": "#f9f9f9",
                                    }
                                ],
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),
                    # UA Matrix (Users and Roles)
                    html.Div(
                        [
                            html.H3("UA Matrix (Users to Roles)"),
                            dash_table.DataTable(
                                id="ua-matrix-table",
                                columns=[],  # Will be populated dynamically
                                data=[],  # Will be populated dynamically
                                style_cell={"textAlign": "left"},
                                sort_action="native",
                                page_size=20,
                                style_data_conditional=[
                                    {
                                        "if": {
                                            "filter_query": '{User} = ""'
                                        },  # Apply to empty rows
                                        "backgroundColor": "#f9f9f9",
                                        "color": "#f9f9f9",
                                    }
                                ],
                            ),
                        ]
                    ),
                    # Calculation time
                    html.Div(id="rmp-calc-time", style={"marginTop": "20px"}),
                ],
            ),
        ],
        style={
            "minWidth": "100%",
            "maxWidth": "100%",
            "width": "100%",
        },
    )
