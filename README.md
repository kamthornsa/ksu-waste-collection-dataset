# KSU Campus Waste-Collection Routing Dataset

Survey data for the paper:

> Khumla, P., Kosasu, J., Sriraksa, N., & Sarawan, K. (2026). *Coverage sets the limit of fixed-route waste collection: exact benchmarking of a priori routing policies.* <!-- TODO: journal / conference, volume, pages, DOI -->

The dataset describes one week of waste collection at the Nai Mueang urban campus of Kalasin University, Thailand: 23 nodes (one vehicle depot, 21 collection points and one waste disposal point), a symmetric road-distance matrix over all 253 node pairs, and the collection sequence actually driven on each of five consecutive days.

It is released so that the five observed daily routing problems can be reproduced and so that the instance can be reused as a small real-world benchmark for path-type TSP and a priori routing studies.

## Repository layout

```
.
├── README.md
├── CITATION.cff
├── LICENSE                      <!-- TODO: add, see "License" below -->
├── data/
│   ├── nodes.csv                 23 nodes with coordinates and roles
│   ├── distance_matrix.csv       23 x 23 road distances (wide format)
│   ├── distance_pairs.csv        same distances, 253 unordered pairs (long format)
│   ├── observed_routes.csv       one row per observed day
│   └── observed_route_stops.csv  one row per stop of each observed route
└── scripts/
    └── validate_data.py          integrity checks (standard library only)
```

`distance_matrix.csv` and `distance_pairs.csv` hold identical values; use whichever shape suits your tooling. The same holds for the two observed-route files. `scripts/validate_data.py` checks that each pair of files agrees.

## Data dictionary

### `data/nodes.csv`

| Column | Type | Description |
|---|---|---|
| `node_id` | integer | Node identifier, 1 to 23. Used as the key in every other file. |
| `facility_name` | text | Name of the building or site. |
| `facility_type` | text | One of `Vehicle depot`, `Teaching building`, `Shared facility`, `Academic staff residence`, `Canteen`, `Disposal point`. |
| `latitude` | decimal degrees | Latitude of the collection point. <!-- TODO: confirm datum (WGS 84?) and how coordinates were recorded --> |
| `longitude` | decimal degrees | Longitude of the collection point. |
| `role` | text | Routing role: `depot` (node 1), `disposal` (node 23) or `collection point` (nodes 2 to 22). |

### `data/distance_matrix.csv`

Square matrix of road distances in **metres**. The first column and the header row are `node_id`s. The matrix is symmetric and the diagonal is 0 (the diagonal was left blank in the original survey workbook).

<!-- TODO: describe how distances were measured (e.g. odometer, GPS track, map service) and how they were validated -->

### `data/distance_pairs.csv`

| Column | Type | Description |
|---|---|---|
| `from_node` | integer | Smaller `node_id` of the pair. |
| `to_node` | integer | Larger `node_id` of the pair. |
| `distance_m` | integer | Road distance in metres (same in both directions). |

### `data/observed_routes.csv`

| Column | Type | Description |
|---|---|---|
| `day_index` | integer | 1 = Monday to 5 = Friday of the observation week. |
| `day` | text | Weekday name. |
| `sequence_driven` | text | Node sequence actually driven, separated by `-`. Every route starts at the depot (1), ends with the disposal point (23) and returns to the depot (1). |
| `nodes_visited` | integer | Number of distinct nodes in the sequence, including depot and disposal point. |

Observation week: <!-- TODO: dates of the survey, e.g. 3–7 March 2025 -->

### `data/observed_route_stops.csv`

| Column | Type | Description |
|---|---|---|
| `day_index` | integer | As above. |
| `day` | text | As above. |
| `stop_order` | integer | Position in the route, starting at 0 for the departure from the depot. |
| `node_id` | integer | Node visited at that position. |

## Problem definition used in the paper

On each day only a subset of the 21 collection points is served. The daily problem is a fixed-start, fixed-end Hamiltonian path: start at the depot (node 1), visit every collection point served that day exactly once, and finish at the disposal point (node 23). The closing leg 23 → 1 has a constant length of 387 m and does not affect which path is optimal.

An a priori (master-sequence) policy fixes one ordering of all 21 collection points and, each day, visits the served points in that order, skipping the rest.

## Quick start

Python (pandas):

```python
import pandas as pd

nodes = pd.read_csv("data/nodes.csv")
D = pd.read_csv("data/distance_matrix.csv", index_col="node_id")
D.columns = D.columns.astype(int)

routes = pd.read_csv("data/observed_routes.csv")
for _, r in routes.iterrows():
    seq = [int(x) for x in r["sequence_driven"].split("-")]
    length = sum(D.at[a, b] for a, b in zip(seq, seq[1:]))
    print(r["day"], length, "m")
```

R:

```r
D <- as.matrix(read.csv("data/distance_matrix.csv", row.names = 1, check.names = FALSE))
routes <- read.csv("data/observed_routes.csv")
```

Check integrity:

```bash
python scripts/validate_data.py
```

## Notes and known limitations

- The matrix records road distances on the campus network. It does not satisfy the triangle inequality for every triple of nodes, so for some pairs a path through a third node is shorter than the recorded direct distance. Solvers that assume metric distances should take this into account. <!-- TODO: explain why (one-way roads, turning restrictions, distance of the route the vehicle must actually take, ...) -->
- The data cover a single week at a single campus and should not be read as representative of other weeks or seasons.
- Waste quantities, vehicle capacity and time windows were not recorded; the instance is a pure distance problem.
- The simulated days and the TSPLIB-based experiments reported in the paper are not stored here. <!-- TODO: link to code repository / supplementary material if released -->

## Changes from the original survey workbook

The CSV files were exported from `Data_available_KSU_Waste_Collection_Survay.xlsx` with these changes only: one file per sheet (plus long-format copies), the blank matrix diagonal filled with 0, a `day_index` column added to the route table, and Windows line endings removed. No distance or coordinate values were altered.

## How to cite

If you use this dataset, please cite the paper above and this repository (see `CITATION.cff`). <!-- TODO: add Zenodo DOI once archived -->

## License

<!-- TODO: choose a license. CC BY 4.0 is common for research data; CC0 1.0 maximises reuse. Add the full text as LICENSE. -->

## Contact

Kamthorn Sarawan, Kalasin University, Thailand — kamthorn.sa@ksu.ac.th
