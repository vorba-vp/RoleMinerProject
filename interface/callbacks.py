import time

import numpy as np
from dash import Dash, Input, Output, State

from algorithms.fast_miner import get_fast_miner_result_with_metadata
from algorithms.rmp import basic_rmp
from dataset import upa_matrix

DATASET_MAPPING = {
    "simple_dataset": "dataset/test_datasets/simple_dataset.txt",
    "identity_matrix": "dataset/test_datasets/identity_matrix.txt",
    "healthcare": "dataset/real_datasets/healthcare.txt",
    "americas_large": "dataset/real_datasets/americas_large.txt",
    "americas_small": "dataset/real_datasets/americas_small.txt",
    "apj": "dataset/real_datasets/apj.txt",
    "customer": "dataset/real_datasets/customer.txt",
    "domino": "dataset/real_datasets/domino.txt",
    "emea": "dataset/real_datasets/emea.txt",
    "firewall-1": "dataset/real_datasets/firewall-1.txt",
    "firewall-2": "dataset/real_datasets/firewall-2.txt",
}


def get_data(dataset: str) -> np.ndarray:
    data = np.array([])  # Default to an empty array if no dataset is selected
    if dataset in DATASET_MAPPING:
        data = upa_matrix.load_upa_from_one2one_file(DATASET_MAPPING[dataset])
    return data


def register_control_callbacks(app: Dash) -> None:
    @app.callback(
        [
            Output("upa-table", "columns"),
            Output("upa-table", "data"),
            Output("upa-table", "style_data_conditional"),
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
                return [], [], [], "Warning: Dataset must be selected", [], [], [], ""

            # Generate columns dynamically based on the data
            columns = [{"name": "U/P", "id": "p_0"}]
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

            # Add padding rows to ensure the table always has 50 rows per page
            page_size = 20
            if len(data_list) > page_size and len(data_list) % page_size != 0:
                # Calculate how many padding rows are needed
                padding_rows = page_size - len(data_list) % page_size
                # Add empty rows for padding
                data_list.extend(
                    [
                        {"p_0": "", **{f"p_{i + 1}": "" for i in range(data.shape[1])}}
                        for _ in range(padding_rows)
                    ]
                )

            # Update the table data, columns
            return (
                columns,
                data_list,
                [],
                "",
            )
        return [], [], [], ""

    @app.callback(
        [
            Output("warning-message", "children"),
            Output("fm-result-table", "columns"),
            Output("fm-result-table", "data"),
            Output("fm-result-table", "selected_rows"),
            Output("calc-time", "children"),
        ],
        [Input("show-fm-button", "n_clicks")],
        [State("dataset-dropdown", "value")],
    )
    def show_fm_result(n_clicks, dataset):
        if n_clicks and n_clicks > 0:
            # Call the function to get the data
            data = get_data(dataset)

            if data.size == 0:
                return "Warning: Dataset must be selected", [], [], [], ""

            fm_result, fm_time = get_fast_miner_result_with_metadata(data)
            fm_result_table_data = [row for row in fm_result.values()]

            page_size = 20
            if (
                len(fm_result_table_data) > page_size
                and len(fm_result_table_data) % page_size != 0
            ):
                # Calculate how many padding rows are needed
                padding_rows = page_size - len(fm_result_table_data) % page_size
                # Add empty rows
                fm_result_table_data.extend(
                    [{"label": "", "original_count": "", "total_count": ""}]
                    * padding_rows
                )

            fm_columns = (
                [
                    {"name": "Label", "id": "label"},
                    {"name": "Original Count", "id": "original_count"},
                    {"name": "Total Count", "id": "total_count"},
                ]
                if fm_result
                else []
            )

            # Update the table data, columns
            return (
                "",
                fm_columns,
                fm_result_table_data,
                [],
                f"Calculation Time: {fm_time} seconds",
            )

        return "", [], [], [], ""

    @app.callback(
        Output(
            "upa-table",
            "style_data_conditional",
            allow_duplicate=True,
        ),
        [Input("fm-result-table", "selected_rows")],
        [State("fm-result-table", "data"), State("upa-table", "data")],
        prevent_initial_call="initial_duplicate",
    )
    def update_styles(selected_rows, dict_data, upa_data):
        style_data_conditional = []

        if selected_rows and dict_data and upa_data:
            selected_row = dict_data[selected_rows[0]]
            selected_permissions = selected_row["label"].split(",")
            selected_columns = [f"p_{int(perm[1:])}" for perm in selected_permissions]

            for upa_row in upa_data:
                if all(upa_row.get(col) == 1 for col in selected_columns):
                    for col in selected_columns:
                        style_data_conditional.append(
                            {
                                "if": {
                                    "filter_query": "{"
                                    + col
                                    + "} = 1 && "
                                    + "{p_0} = "
                                    + upa_row["p_0"],
                                    "column_id": col,
                                },
                                "backgroundColor": "#FFDDC1",
                                "color": "black",
                            }
                        )
        return style_data_conditional

    @app.callback(
        [
            Output("pa-matrix-table", "columns"),
            Output("pa-matrix-table", "data"),
            Output("ua-matrix-table", "columns"),
            Output("ua-matrix-table", "data"),
            Output("rmp-calc-time", "children"),
        ],
        [Input("show-brmp-button", "n_clicks")],
        [State("dataset-dropdown", "value"), State("upa-table", "data")],
    )
    def update_rmp_results(n_clicks, dataset, upa_table_data):
        if n_clicks and dataset:
            # Retrieve the UPA matrix data from the selected dataset
            data = get_data(dataset)

            if data.size == 0:
                return [], [], [], [], "Warning: Invalid dataset selected."

            # Run the RMP algorithm
            start_time = time.time()
            pa_matrix, ua_matrix = basic_rmp(data)
            calc_time = time.time() - start_time

            # Prepare PA matrix data for display
            pa_matrix_data = [
                {"Role": k, "Permissions": ", ".join(v)} for k, v in pa_matrix.items()
            ]
            pa_columns = [
                {"name": "Role", "id": "Role"},
                {"name": "Permissions", "id": "Permissions"},
            ]

            # Prepare UA matrix data for display
            ua_matrix_data = [
                {"User": k, "Roles": ", ".join(v)} for k, v in ua_matrix.items()
            ]
            ua_columns = [
                {"name": "User", "id": "User"},
                {"name": "Roles", "id": "Roles"},
            ]

            page_size = 20
            if len(ua_matrix_data) > page_size and len(ua_matrix_data) % page_size != 0:
                # Calculate how many padding rows are needed
                padding_rows = page_size - len(ua_matrix_data) % page_size
                # Add empty rows
                ua_matrix_data.extend([{"User": "", "Roles": ""}] * padding_rows)

            if len(pa_matrix_data) > page_size and len(pa_matrix_data) % page_size != 0:
                # Calculate how many padding rows are needed
                padding_rows = page_size - len(pa_matrix_data) % page_size
                # Add empty rows
                pa_matrix_data.extend([{"Role": "", "Permissions": ""}] * padding_rows)

            return (
                pa_columns,
                pa_matrix_data,
                ua_columns,
                ua_matrix_data,
                f"RMP Calculation Time: {calc_time:.2f} seconds",
            )

        return [], [], [], [], ""

    @app.callback(
        Output(
            "result-area", "children"
        ),  # Replace 'children' with your table content, if needed
        Input("clear-button", "n_clicks"),
    )
    def clear_output(n_clicks):
        if n_clicks > 0:
            return []
