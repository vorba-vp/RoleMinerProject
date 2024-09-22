import os

from dash import dash, html

from interface.callbacks import register_control_callbacks
from interface.layouts.control_panel import control_panel_layout
from interface.layouts.fast_miner_part import get_fast_miner_result_layout
from interface.layouts.rmp_results_part import get_rmp_results_layout
from interface.layouts.upa_matrix_part import get_upa_matrix_layout

PAGE_SIZE = 20


def main() -> dash.Dash:
    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            # Upper control panel section
            control_panel_layout,
            # Bottom section divided into two parts
            html.Div(
                children=[
                    get_upa_matrix_layout(),
                    html.Hr(style={"border": "1px solid #000", "margin": "20px 0"}),
                    get_fast_miner_result_layout(),
                    html.Hr(style={"border": "1px solid #000", "margin": "20px 0"}),
                    get_rmp_results_layout(),
                ],
                id="result-area",
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
