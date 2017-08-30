import cxmate
import logging

import numpy as np

from graph_tool import all as gt


logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)


from cxmate.cxmate_pb2 import NetworkElement
from cxmate.service import NetworkElementBuilder


class GtLayoutService(cxmate.Service):

    def __prob(self, a, b):
        if a == b:
            return 0.999
        else:
            return 0.001

    def process(self, params, input_stream):
        logger.warn(params)

        # Toy example: generate random graph
        g, bm = gt.random_graph(3000, lambda: np.random.poisson(10), directed=False,
                                model = "blockmodel",
                                block_membership = lambda: np.random.randint(10),
                                edge_probs = self.__prob)

        pos = gt.sfdp_layout(g, groups=bm)

        return self.__create_output_stream(g, pos)


    def __create_node(self, nodeId, name):
        ele = NetworkElement()
        ele.label = 'out_net'
        node = ele.node
        node.id = nodeId
        node.name = name
        return ele

    def __create_edge(self, edgeId, sourceId, targetId, interaction):
        ele = NetworkElement()
        ele.label = 'out_net'
        edge = ele.edge
        edge.id = edgeId
        edge.sourceId = sourceId
        edge.targetId = targetId
        edge.interaction = interaction
        return ele


    def __create_output_stream(self, g, pos):

        nodes = g.get_vertices()
        edges = g.edges()


        for nodeId in nodes:
            yield self.__create_node(nodeId, str(nodeId))

        for i, e in enumerate(edges):
            yield self.__create_edge(i, int(e.source()), int(e.target()), 'itr')

        for v in nodes:
            position = pos[g.vertex(v)]
            ele = NetworkElement()

            ele.label = 'out_net'
            coord = ele.CartesianCoordinate
            coord.nodeId = v
            coord.x = position[0]*2000
            coord.y = position[1]*2000

            yield ele


if __name__ == "__main__":
    analyzer = GtLayoutService()
    logger.info('Starting graph-tool analysis service...')
    analyzer.run()
