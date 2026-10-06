import json
import numpy as np


with open("mock_data/15/measurement_001.json") as f:
    data = json.load(f)

obfuscation_threshold = data["obfuscation_threshold"]

# First measurement
measurement = data["measurements"][0]

# First 15-minute interval
interval = measurement["results"]["data"][0]
counts = interval["counts"]


# Get origins and destinations
in_indexes = list(counts.keys())

out_indexes = sorted({
    port_out
    for out_counts in counts.values()
    for port_out in out_counts
})


# Create OD matrix
od_matrix = np.full(
    (len(in_indexes), len(out_indexes)),
    None,
    dtype=object
)


# Fill matrix with car counts
for i, port_in in enumerate(in_indexes):
    for j, port_out in enumerate(out_indexes):

        # No entry for this origin/destination pair
        if port_out not in counts[port_in]:
            od_matrix[i, j] = 0
            continue

        # Get car count
        od_matrix[i, j] = counts[port_in][port_out]["car"]


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