import cxmate
import logging
import itertools

import numpy as np
from graph_tool import all as gt

logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)

from Adapter import Adapter


class GtLayoutService(cxmate.Service):

    def __prob(self, a, b):
        if a == b:
            return 0.999
        else:
            return 0.001

    def process(self, params, input_stream):
        logger.warn(params)

        # Toy example: generate random graph
        # g, bm = gt.random_graph(1000, lambda: np.random.poisson(10), directed=False,
        #                         model = "blockmodel",
        #                         block_membership = lambda: np.random.randint(10),
        #                         edge_probs = self.__prob)
        g = gt.price_network(3000)
        gl = [g]
        # g = Adapter.to_graph_tool(input_stream)
        if params["with-position"]:
            pos = gt.sfdp_layout(g)
            # pos = gt.sfdp_layout(g, groups=bm)
            return Adapter.from_graph_tool(gl, pos)
        else:
            return Adapter.from_graph_tool(gl)


if __name__ == "__main__":
    analyzer = GtLayoutService()
    logger.info('Starting graph-tool analysis service...')
    analyzer.run()
