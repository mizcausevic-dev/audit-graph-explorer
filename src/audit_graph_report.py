from __future__ import annotations

import json
from collections import Counter, deque, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "data" / "graph_snapshot.json"


def load_snapshot(path: Path = SNAPSHOT_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_indexes(snapshot: dict) -> Tuple[Dict[str, dict], Dict[str, List[Tuple[str, str]]]]:
    nodes = {node["id"]: node for node in snapshot["nodes"]}
    adjacency: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for edge in snapshot["edges"]:
        adjacency[edge["from"]].append((edge["to"], edge["type"]))
        adjacency[edge["to"]].append((edge["from"], edge["type"]))
    return nodes, adjacency


def shortest_path(nodes: Dict[str, dict], adjacency: Dict[str, List[Tuple[str, str]]], start: str, goal: str) -> List[dict]:
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return [{"id": current, "label": nodes[current]["label"], "type": nodes[current]["type"]} for current in [start] + [step["id"] for step in path]]
        for neighbor, rel_type in adjacency[current]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append(
                (
                    neighbor,
                    path
                    + [
                        {
                            "id": neighbor,
                            "label": nodes[neighbor]["label"],
                            "type": nodes[neighbor]["type"],
                            "via": rel_type,
                        }
                    ],
                )
            )
    return []


def find_path(nodes: Dict[str, dict], adjacency: Dict[str, List[Tuple[str, str]]], start: str, goal: str) -> List[dict]:
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return [{"id": start, "label": nodes[start]["label"], "type": nodes[start]["type"]}] + path
        for neighbor, rel_type in adjacency[current]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append(
                (
                    neighbor,
                    path
                    + [
                        {
                            "id": neighbor,
                            "label": nodes[neighbor]["label"],
                            "type": nodes[neighbor]["type"],
                            "via": rel_type,
                        }
                    ],
                )
            )
    return []


def blast_radius(nodes: Dict[str, dict], adjacency: Dict[str, List[Tuple[str, str]]], start: str, max_depth: int = 3) -> List[dict]:
    queue = deque([(start, 0)])
    seen = {start}
    findings = []
    while queue:
        current, depth = queue.popleft()
        if depth == max_depth:
            continue
        for neighbor, rel_type in adjacency[current]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((neighbor, depth + 1))
            node = nodes[neighbor]
            if node["type"] in {"Asset", "Incident", "Exception"}:
                findings.append(
                    {
                        "id": neighbor,
                        "label": node["label"],
                        "type": node["type"],
                        "depth": depth + 1,
                        "via": rel_type,
                    }
                )
    findings.sort(key=lambda item: (item["depth"], item["type"], item["id"]))
    return findings


def owner_pressure(snapshot: dict) -> List[dict]:
    edges = snapshot["edges"]
    ownership = defaultdict(list)
    nodes = {node["id"]: node for node in snapshot["nodes"]}
    for edge in edges:
        if edge["type"] == "OWNED_BY" and edge["from"].startswith("exception-"):
            ownership[edge["to"]].append(edge["from"])
    rows = []
    for owner_id, exception_ids in ownership.items():
        owner = nodes[owner_id]
        rows.append(
            {
                "owner": owner["label"],
                "role": owner.get("role", ""),
                "exceptions": len(exception_ids),
                "items": exception_ids,
            }
        )
    return sorted(rows, key=lambda item: (-item["exceptions"], item["owner"]))


def build_report(snapshot: dict | None = None) -> dict:
    snapshot = snapshot or load_snapshot()
    nodes, adjacency = build_indexes(snapshot)
    type_counts = Counter(node["type"] for node in snapshot["nodes"])
    open_exceptions = [n for n in snapshot["nodes"] if n["type"] == "Exception" and n["status"] in {"open", "watch"}]
    active_incidents = [n for n in snapshot["nodes"] if n["type"] == "Incident" and n["status"] in {"watch", "investigating"}]
    critical_assets = [n for n in snapshot["nodes"] if n["type"] == "Asset" and n.get("tier") == "tier-0"]
    path = find_path(nodes, adjacency, "exception-233", "asset-admin-console")
    vendor_blast = blast_radius(nodes, adjacency, "vendor-acme", max_depth=4)
    pressure = owner_pressure(snapshot)
    return {
        "headline": "Graph explainability for governance, identity, and vendor-linked audit pressure.",
        "summary": {
            "node_count": len(snapshot["nodes"]),
            "edge_count": len(snapshot["edges"]),
            "open_exceptions": len(open_exceptions),
            "active_incidents": len(active_incidents),
            "critical_assets": len(critical_assets),
        },
        "type_counts": dict(type_counts),
        "path": path,
        "blast_radius": vendor_blast,
        "owner_pressure": pressure,
        "priority_note": "Vendor-linked access pressure reaches a tier-0 asset through an approved exception chain. The graph makes the ownership path visible immediately.",
    }


def write_report(path: Path) -> dict:
    report = build_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

