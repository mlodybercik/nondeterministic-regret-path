import typing as T

import numpy as np
import pygame.draw as draw
from numpy.typing import NDArray

if T.TYPE_CHECKING:
    from pygame.surface import Surface

    from ..solver.graph import NDEdge, NDGraph, NDNode


class Draw:
    graph: "NDGraph"
    positions: T.Dict["NDNode", NDArray[2]]
    path_overrides: T.Set["NDEdge"]
    path_hash: T.Set[int]

    def __init__(self, graph, positions) -> None:
        self.graph = graph
        self.positions = positions
        self.set_overrides([])

    def set_overrides(self, override):
        self.path_overrides = set(override)
        self.path_hash = {hash(i) for i in override}

    def draw_nodes(self, surface: "Surface"):
        size = np.array(surface.get_size())
        overriden_nodes = {node.source for node in self.path_overrides} | {node.target for node in self.path_overrides}
        for node, position in self.positions.items():
            color = (0x3F, 0x3F, 0x3F)
            if node in overriden_nodes:
                color = (0xFF, 0xFF, 0xFF)
            draw.circle(surface, color, position * size, 10, width=0)

    def draw_edges(self, surface: "Surface"):
        size = np.array(surface.get_size())
        for edge in self.graph.edges:
            color = (0x3F, 0x3F, 0x3F)
            if hash(edge) in self.path_hash:
                color = (0xFF, 0xFF, 0xFF)
            draw.line(surface, color, self.positions[edge.source] * size, self.positions[edge.target] * size, 2)
