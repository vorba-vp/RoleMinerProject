import os

from dash import dash, html

from interface.callbacks import register_control_callbacks
from interface.layouts.control_panel import control_panel_layout
from interface.layouts.left_part import upa_matrix_layout
from interface.layouts.right_part import fast_miner_result_layout


def main() -> dash.Dash:
    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            # Upper control panel section
            control_panel_layout,
            # Bottom section divided into two parts
            html.Div(
                children=[
                    # Left part of the bottom section
                    upa_matrix_layout,
                    # Right part of the bottom section
                    fast_miner_result_layout,
                ],
                style={"display": "flex", "flex-direction": "column"},
            ),
        ]
    )

    # Import callbacks after app and layout have been defined
    register_control_callbacks(app)

    return app


if __name__ == "__main__":
    app = main()
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
