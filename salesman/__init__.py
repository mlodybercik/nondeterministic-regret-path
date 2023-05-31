import logging

from .solver.graph import NDEdge, NDGraph, NDNode
from .solver.solver import RegretSolver

# from .viewer.window import Window

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(ch)

__all__ = ["NDEdge", "NDGraph", "NDNode", "Window", "RegretSolver"]
