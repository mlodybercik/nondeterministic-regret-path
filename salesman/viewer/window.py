from typing import TYPE_CHECKING, Tuple

import pygame as pg

from . import logger

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

    def render_frame(self) -> "pg.Surface":
        pass

    def loop(self):
        screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            screen.blit(self.render_frame(), (0, 0))
            clock.tick(60)
