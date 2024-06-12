from dash import dash_table, html

left_part_layout = html.Div(
    children=[
        html.H2("Left Part"),
        dash_table.DataTable(
            id="upa-table",
            columns=[],
            data=[],
            style_table={"overflowX": "auto"},
            fixed_columns={"headers": True, "data": 1},
            style_cell={
                "textAlign": "center",
                "minWidth": "50px",
                "maxWidth": "50px",
                "width": "50px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
            style_cell_conditional=[
                {
                    "if": {"column_id": "p_0"},
                    "minWidth": "85px",
                    "maxWidth": "85px",
                    "width": "85px",
                }
            ],
        ),
    ],
    style={"width": "50%"},
)
