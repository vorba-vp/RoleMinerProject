from dash import dash, html

from interface.callbacks import register_control_callbacks
from interface.layouts.control_panel import control_panel_layout
from interface.layouts.left_part import left_part_layout


def main():
    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            # Upper control panel section
            control_panel_layout,
            # Bottom section divided into two parts
            html.Div(
                children=[
                    # Left part of the bottom section
                    left_part_layout,
                    # Right part of the bottom section
                    html.Div(
                        children=[
                            html.H2("Right Part"),
                            # Add content for the right part here
                        ],
                        style={"width": "50%"},
                    ),
                ],
                style={"display": "flex", "height": "80vh"},
            ),
        ]
    )

    # Import callbacks after app and layout have been defined
    register_control_callbacks(app)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
