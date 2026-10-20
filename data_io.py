import json
import os
from typing import Literal, TypedDict

VehicleType = Literal["car", "truck", "motorcycle"]
PortlineNameIn = Literal["north_in", "east_in", "south_in", "west_in"]
PortlineNameOut = Literal["north_out", "east_out", "south_out", "west_out"]
ObfuscationMethod = Literal["null_below_threshold"]

class Position(TypedDict):
    x: float
    y: float

class Portline(TypedDict):
    name: PortlineNameIn | PortlineNameOut
    start: Position
    end: Position

class Coordinates(TypedDict):
    lat: float
    lon: float

class Site(TypedDict):
    site_id: str
    name: str
    location: Coordinates
    portlines: list[Portline]
    pedestrian_polygons: list[None] # TODO: Implement this

Counts = dict[PortlineNameIn, dict[PortlineNameOut, dict[VehicleType, int | None]]]

class Interval(TypedDict):
    interval_start: str
    interval_end: str
    counts: Counts

class Results(TypedDict):
    interval_start: str
    interval_end: str
    data: list[Interval]

class Measurement(TypedDict):
    measurement_id: str
    start_time: str
    end_time: str
    site: Site
    results: Results

class Dataset(TypedDict):
    schema_version: str
    aggregation_interval_minutes: int
    obfuscation_threshold: int
    obfuscation_method: ObfuscationMethod
    measurements: list[Measurement]

def load_dataset(data_path: str) -> Dataset:
    with open(data_path) as f:
        return json.load(f)

def load_datasets(data_paths: tuple[str, ...]) -> dict[str, Dataset]:
    # Parses datapaths ending with "/*"
    data_paths_expanded = (i for p in data_paths for i in ((p[:-1] + i for i in os.listdir(p[:-2])) if p.endswith("/*") else (p,)))

    return {data_path: load_dataset(data_path) for data_path in data_paths_expanded}