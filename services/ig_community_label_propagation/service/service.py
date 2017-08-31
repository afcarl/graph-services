import cxmate
import logging

import igraph as ig
from igraph_adapter import *

logger = logging.getLogger('igraph_service')
logger.setLevel(logging.INFO)

from cxmate.cxmate_pb2 import NetworkElement


class IgStatisticsService(cxmate.Service):

    def process(self, params, input_stream):
        logging.info(params)

        ig_network = IgraphAdapter.to_igraph(input_stream)
        pr = ig_network.pagerank(vertices=ig_network.vs)
        ig_network.vs['pagerank'] = pr
        ig_network['label'] = 'out_net'

        return IgraphAdapter.from_igraph(ig_network)

    def __create_output_stream(self, vs):
        for v in vs:
            ele = NetworkElement()
            ele.label = 'out_net'
            nodeAttr = ele.nodeAttribute
            nodeAttr.nodeId = v['name']
            nodeAttr.name = 'pagerank'
            nodeAttr.type = 'double'
            nodeAttr.value = str(v['pagerank'])
            yield ele


if __name__ == "__main__":

    analyzer = IgStatisticsService()
    logging.warn('Starting igraph analysis service...')
    analyzer.run()
