import numpy as np
from dash import Dash, Input, Output, State

from dataset import upa_matrix


def get_data(dataset: str) -> np.ndarray:
    if dataset == "simple_dataset":
        data = upa_matrix.load_upa_from_one2one_file(
            "dataset/test_datasets/simple_dataset.txt"
        )
    elif dataset == "identity_matrix":
        data = upa_matrix.load_upa_from_one2one_file(
            "dataset/test_datasets/identity_matrix.txt"
        )
    else:
        data = np.array([])  # Default to an empty array if no dataset is selected
    return data


def register_control_callbacks(app: Dash) -> None:

    @app.callback(
        [
            Output("upa-table", "columns"),
            Output("upa-table", "data"),
            Output("warning-message", "children"),
        ],
        [Input("show-upa-button", "n_clicks")],
        [State("dataset-dropdown", "value")],
    )
    def show_upa(n_clicks, dataset):
        if n_clicks and n_clicks > 0:
            # Call the function to get the data
            data = get_data(dataset)

            if data.size == 0:
                return [], [], "Warning: Dataset must be selected"

            # Generate columns dynamically based on the data
            columns = [{"name": "Users/Permissions", "id": "p_0"}]
            columns.extend(
                [
                    {"name": f"P{i + 1}", "id": f"p_{i + 1}"}
                    for i in range(data.shape[1])
                ]
            )

            # Convert ndarray to list of dictionaries for Dash DataTable
            data_list = [
                {
                    **{"p_0": f"U{index + 1}"},
                    **dict(zip([f"p_{i + 1}" for i in range(data.shape[1])], row)),
                }
                for index, row in enumerate(data)
            ]

            # Update the table data, columns
            return columns, data_list, ""
        return [], [], ""
