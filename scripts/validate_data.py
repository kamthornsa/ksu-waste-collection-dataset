"""Validate the integrity of the released dataset.

Run from the repository root:  python scripts/validate_data.py
Uses only the Python standard library.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


nodes = read("nodes.csv")
node_ids = [int(r["node_id"]) for r in nodes]
assert node_ids == list(range(1, 24)), "node_id must be 1..23"
roles = {int(r["node_id"]): r["role"] for r in nodes}
assert roles[1] == "depot" and roles[23] == "disposal"

# Distance matrix: square, zero diagonal, symmetric, positive off-diagonal
with open(DATA / "distance_matrix.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))
header = [int(x) for x in rows[0][1:]]
D = {int(r[0]): {h: int(v) for h, v in zip(header, r[1:])} for r in rows[1:]}
assert header == node_ids and sorted(D) == node_ids
for i in node_ids:
    assert D[i][i] == 0
    for j in node_ids:
        assert D[i][j] == D[j][i], f"asymmetric at ({i},{j})"
        if i != j:
            assert D[i][j] > 0

# Long format must agree with the matrix (253 = 23*22/2 pairs)
pairs = read("distance_pairs.csv")
assert len(pairs) == 253
for p in pairs:
    assert D[int(p["from_node"])][int(p["to_node"])] == int(p["distance_m"])

# Observed routes: start at depot, end with disposal -> depot, no repeated stop
for r in read("observed_routes.csv"):
    seq = [int(x) for x in r["sequence_driven"].split("-")]
    assert seq[0] == 1 and seq[-2:] == [23, 1], f"{r['day']}: bad endpoints"
    assert len(set(seq[:-1])) == len(seq) - 1, f"{r['day']}: repeated node"
    assert set(seq) <= set(node_ids)
    length = sum(D[a][b] for a, b in zip(seq, seq[1:]))
    distinct = len(set(seq))
    flag = "" if distinct == int(r["nodes_visited"]) else "  <-- nodes_visited mismatch"
    print(f"{r['day']:<10} distinct nodes={distinct:>2}  "
          f"nodes_visited={r['nodes_visited']:>2}  length={length:>5} m{flag}")

print("Basic checks passed.")
