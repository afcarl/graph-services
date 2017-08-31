import cxmate
import logging

import igraph as ig
from igraph_adapter import *

logger = logging.getLogger('igraph_service')
logger.setLevel(logging.INFO)


from cxmate.cxmate_pb2 import NetworkElement


class IgStatisticsService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)


        stat_type  = params['stat-name']

        ig_network = IgraphAdapter.to_igraph(input_stream)

        if stat_type == 'edge-betweenness':
            ig_network.es['edge-betweenness'] = ig_network.edge_betweenness()
            return self.__create_output_stream_edge(ig_network.es)
        else:
            ig_network.vs['pagerank'] = ig_network.pagerank(vertices=ig_network.vs)
            return self.__create_output_stream(ig_network.vs)


    def __create_output_stream_edge(self, es):
        for e in es:
            ele = NetworkElement()
            ele.label = 'out_net'
            edgeAttr = ele.edgeAttribute
            edgeAttr.edgeId = e['eid']
            edgeAttr.name = 'edge-betweenness'
            edgeAttr.type = 'double'
            edgeAttr.value = str(e['edge-betweenness'])
            yield ele


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
