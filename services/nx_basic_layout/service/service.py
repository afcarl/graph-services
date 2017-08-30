import networkx as nx
import cxmate
import logging

from cxmate.cxmate_pb2 import NetworkElement


class BasicLayoutService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)

        # Get the type of the analysis
        layout_name = params['layout-name']

        networks = cxmate.Adapter.to_networkx(input_stream)

        for net in networks:
            # Calculate layout for the first network
            pos = self.__get_layout(net, layout_name)
            return self.__output_stream(pos)

    def __get_layout(self, net, layout_type):
        if layout_type == 'circular':
            return nx.circular_layout(net)
        elif layout_type == 'spring':

            return nx.spring_layout(net)
        else:
            return nx.circular_layout(net)

    def __output_stream(self, pos):
        for k in pos.keys():
            ele = NetworkElement()
            ele.label = 'out_net'
            coord = ele.CartesianCoordinate
            coord.nodeId = k
            coord.x = pos[k][0]
            coord.y = pos[k][1]
            yield ele


if __name__ == "__main__":

    analyzer = BasicLayoutService()
    logging.warn('Starting graph analysis service...')
    analyzer.run()
