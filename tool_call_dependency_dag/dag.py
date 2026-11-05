"""Topological dependency DAG scheduler for tool execution."""
from collections import defaultdict, deque
from typing import Dict, List, Any, Callable, Set


class ToolDependencyDAG:
    def __init__(self):
        self._nodes: Dict[str, Callable[..., Any]] = {}
        self._deps: Dict[str, Set[str]] = defaultdict(set)

    def add_tool_step(self, step_id: str, fn: Callable[..., Any], depends_on: List[str]):
        self._nodes[step_id] = fn
        self._deps[step_id] = set(depends_on)

    def get_execution_waves(self) -> List[List[str]]:
        in_degree = {k: len(deps) for k, deps in self._deps.items()}
        for k in self._nodes:
            if k not in in_degree:
                in_degree[k] = 0

        queue = deque([k for k, deg in in_degree.items() if deg == 0])
        waves = []

        visited_count = 0
        while queue:
            current_wave = list(queue)
            waves.append(current_wave)
            queue.clear()
            for node in current_wave:
                visited_count += 1
                for neighbor, deps in self._deps.items():
                    if node in deps:
                        in_degree[neighbor] -= 1
                        if in_degree[neighbor] == 0:
                            queue.append(neighbor)

        if visited_count != len(self._nodes):
            raise ValueError("Dependency cycle detected in DAG")

        return waves

    def execute(self) -> Dict[str, Any]:
        waves = self.get_execution_waves()
        results = {}
        for wave in waves:
            for node in wave:
                results[node] = self._nodes[node](results)
        return results
