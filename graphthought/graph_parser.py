import re
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GraphNode:
    node_id: int
    proposition: str
    conclusion: Optional[str]
    dependencies: list = field(default_factory=list)

@dataclass
class ReasoningGraph:
    nodes: dict = field(default_factory=dict)
    answer: Optional[str] = None
    is_valid: bool = True

def parse_gsf(text: str) -> ReasoningGraph:
    graph = ReasoningGraph()
    node_pattern = re.compile(
        r'\[NODE\s+(\d+)(?:\|dep:([\d,]+))?\]\s*(.+?)(?:\s*→\s*(.+))?$',
        re.MULTILINE
    )
    answer_pattern = re.compile(r'\[ANSWER(?:\|dep:[\d,]+)?\]\s*(.+)$', re.MULTILINE)

    for match in node_pattern.finditer(text):
        node_id = int(match.group(1))
        deps_raw = match.group(2)
        proposition = match.group(3).strip()
        conclusion = match.group(4).strip() if match.group(4) else None
        deps = [int(d.strip()) for d in deps_raw.split(',')] if deps_raw else []
        graph.nodes[node_id] = GraphNode(node_id, proposition, conclusion, deps)

    answer_match = answer_pattern.search(text)
    if answer_match:
        graph.answer = answer_match.group(1).strip()

    graph.is_valid = not _has_cycle(graph.nodes)
    return graph

def _has_cycle(nodes: dict) -> bool:
    visited, rec_stack = set(), set()
    def dfs(nid):
        visited.add(nid); rec_stack.add(nid)
        for dep in nodes.get(nid, GraphNode(nid, "", None)).dependencies:
            if dep not in visited:
                if dfs(dep): return True
            elif dep in rec_stack:
                return True
        rec_stack.discard(nid)
        return False
    for nid in nodes:
        if nid not in visited:
            if dfs(nid): return True
    return False

def topological_layers(graph: ReasoningGraph) -> list:
    layers, resolved = [], set()
    while len(resolved) < len(graph.nodes):
        layer = [
            nid for nid, node in graph.nodes.items()
            if nid not in resolved
            and all(dep in resolved for dep in node.dependencies)
        ]
        if not layer:
            break
        layers.append(layer)
        resolved.update(layer)
    return layers
