from typing import TYPE_CHECKING, Tuple

import pygame as pg

from . import logger
from .drawer import Draw

if TYPE_CHECKING:
    from ..solver.graph import NDGraph

pg.init()


class Window:
    size: Tuple[int, int]
    graph: "NDGraph"
    running: bool

    def __init__(self, size: Tuple[int, int], title: str) -> None:
        logger.info(f"Creating window size: {size}")
        self.running = True
        self.size = size
        pg.display.set_caption(title)

    def render_frame(self, drawer: "Draw") -> "pg.Surface":
        logger.debug("Drawing new frame")
        surface = pg.Surface(self.size)
        drawer.draw_edges(surface)
        drawer.draw_nodes(surface)
        return surface

    def loop(self):
        screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()
        drawer = Draw(self.graph, self.graph.get_spring_layout())
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            screen.blit(self.render_frame(drawer), (0, 0))
            pg.display.flip()
            dt = clock.tick(60)
            if (dt / 1000) - (1 / 60) > 10:
                logger.warning("Frame took longer than 10ms")
