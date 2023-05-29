from typing import TYPE_CHECKING, Tuple

import pygame as pg

from . import logger
from .drawer import Draw

if TYPE_CHECKING:
    from ..solver.graph import NDGraph
    from ..solver.solver import RegretSolver

pg.init()

FPS = 120


class Window:
    size: Tuple[int, int]
    graph: "NDGraph"
    running: bool

    def __init__(self, size: Tuple[int, int], title: str, solver: "RegretSolver") -> None:
        logger.info(f"Creating window size: {size}")
        self.running = True
        self.size = size
        self.solver = solver
        pg.display.set_caption(title)

    def render_frame(self, drawer: "Draw") -> "pg.Surface":
        surface = pg.Surface(self.size)
        drawer.draw_edges(surface)
        drawer.draw_nodes(surface)
        return surface

    def loop(self):
        screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()
        drawer = Draw(self.graph, self.graph.get_spring_layout(0.01, 100))
        generator = self.solver.iterator()
        path, value = next(generator)
        best_path = value
        space_held = False
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    space_held = True
            if space_held:
                path, value = next(generator)
                if value < best_path:
                    pg.display.set_caption(f"best path: {value}")
                    best_path = value
                    min_path = sum([edge.min_length for edge in path])
                    real_path = sum([edge.length for edge in path])
                    max_path = sum([edge.max_length for edge in path])
                    logger.info(
                        f"Found better path ||{real_path:02.2f}||, ||{min_path:02.2f}||min ||{max_path:02.2f}||max"
                    )
                    space_held = False
                drawer.set_overrides(path)
            screen.blit(self.render_frame(drawer), (0, 0))
            pg.display.flip()
            dt = clock.tick(FPS)
            if (dt / 1000) - (1 / FPS) > 10:
                logger.warning("Frame took longer than 10ms")
