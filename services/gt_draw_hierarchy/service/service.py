import cxmate
import logging

import numpy as np
from graph_tool import all as gt

logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)

from Adapter import Adapter


class GtDrawHierarchyService(cxmate.Service):
    def __init__(self):
        self.parameter = ["layout"]

    def process(self, params, input_stream):
        logger.warn(params)

        parameter = {p: params[p] for p in self.parameter}
        g = Adapter.to_graph_tool(input_stream)
        state = gt.minimize_nested_blockmodel_dl(g[0], deg_corr=True)
        pos, t, tpos = gt.draw_hierarchy(state, output="output.pdf", **parameter)
        # return Adapter.from_graph_tool(g, pos, params["only-layout"])
        return Adapter.from_graph_tool([t], tpos, params["only-layout"])


if __name__ == "__main__":
    analyzer = GtDrawHierarchyService()
    logger.info('Starting graph-tool analysis service...')
    analyzer.run()
