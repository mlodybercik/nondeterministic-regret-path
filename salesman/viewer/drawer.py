from typing import TYPE_CHECKING, Dict

import numpy as np
import pygame.draw as draw
from numpy.typing import NDArray

if TYPE_CHECKING:
    from pygame.surface import Surface

    from ..solver.graph import NDGraph, NDNode


class Draw:
    graph: "NDGraph"
    positions: Dict["NDNode", NDArray[2]]

    def __init__(self, graph, positions) -> None:
        self.graph = graph
        self.positions = positions

    def draw_nodes(self, surface: "Surface"):
        size = np.array(surface.get_size())
        for node, position in self.positions.items():
            draw.circle(surface, (0xFF, 0xFF, 0xFF), position * size, 10, width=0)

    def draw_edges(self, surface: "Surface"):
        size = np.array(surface.get_size())
        for edge in self.graph.edges:
            draw.aaline(
                surface, (0xF0, 0xF0, 0xF0), self.positions[edge.source] * size, self.positions[edge.target] * size
            )
