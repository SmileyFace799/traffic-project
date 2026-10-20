import numpy as np
from typing import Literal
from data_io import *

# Changge what to load
data_paths : tuple[str, ...] = ("mock_data/15/*",)
exclude_measurements : dict[str, tuple[int, ...]] = {
    "mock_data/15/measurement_001.json": (0,)
}
vehicle_type : VehicleType = "car"

# Load selected datasets, get global info
datasets = load_datasets(data_paths)


for name, dataset in datasets.items():
    obfuscation_threshold = dataset["obfuscation_threshold"]
    for measurement in dataset["measurements"]:
        in_indexes: list[PortlineNameIn] = []
        out_indexes: list[PortlineNameOut] = []

        od_dict : dict[PortlineNameIn, dict[PortlineNameOut, int | None]] = {}

        for interval in measurement["results"]["data"]:
            counts = interval["counts"]

            # Get origins and destinations
            for k_in in counts.keys():
                if k_in not in in_indexes:
                    in_indexes.append(k_in)
                    od_dict[k_in] = {}

                for k_out in counts[k_in]:
                    if k_out not in out_indexes:
                        out_indexes.append(k_out)
                    if k_out not in od_dict[k_in].keys():
                        od_dict[k_in][k_out] = 0

                    count = counts[k_in][k_out][vehicle_type]
                    if count is None:
                        od_dict[k_in][k_out] = None
                    elif (v := od_dict[k_in][k_out]) is not None: # Variable assignment to satisfy type checker
                        od_dict[k_in][k_out] = v + count

        in_indexes.sort()
        out_indexes.sort()

        # Create OD matrix
        od_matrix = np.full(
            (len(in_indexes), len(out_indexes)),
            None,
            dtype=object
        )

        # Fill matrix with car counts
        for i, k_in in enumerate(in_indexes):
            for j, k_out in enumerate(out_indexes):

                # No entry for this origin/destination pair
                if k_out not in od_dict[k_in]:
                    od_matrix[i, j] = 0
                    continue

                # Get car count
                od_matrix[i, j] = od_dict[k_in][k_out]

        # Print matrix
        print("Car OD matrix")
        print()

        # Header
        print(f"{'Origin':12}", end="")
        for port_out in out_indexes:
            print(f"{port_out:>12}", end="")
        print()

        # Rows
        for i, port_in in enumerate(in_indexes):
            print(f"{port_in:12}", end="")

            for j in range(len(out_indexes)):
                value = od_matrix[i, j]

                if value is None:
                    display = "NULL"
                else:
                    display = str(value)

                print(f"{display:>12}", end="")

            print()