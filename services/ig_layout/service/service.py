import cxmate
import logging
import igraph as ig
from Adapter import NetworkElementBuilder, IgraphAdapter
from handlers import IgLayoutHandlers

logger = logging.getLogger('igraph_service')
logging.basicConfig(level=logging.DEBUG)

# Label for CXmate output
OUTPUT_LABEL = 'out_net'

# Community detection algorithm name
ALGORITHM_TYPE = 'layout'


class IgLayoutService(cxmate.Service):

    def __init__(self):
        self.__handlers = IgLayoutHandlers()

    def process(self, params, input_stream):
        algorithm_type = params[ALGORITHM_TYPE]
        del params[ALGORITHM_TYPE]

        # Replace string None to Python None data type
        for k, v in params.items():
            if v == str(None):
                params[k] = None

        # Convert to igraph objects
        ig_networks = IgraphAdapter.to_igraph(input_stream)
        pos_dict = {}

        for net in ig_networks:
            net['label'] = OUTPUT_LABEL

            # Get the layout function by name of the algorithm
            handler = self.__handlers.get_handler(algorithm_type)

            # Call the function to calculate layout
            pos = handler(net, **params)

            for i, vertex in enumerate(net.vs):
                pos_dict[vertex['nodeId']] = pos[i]

        return self.outputStream(ig_networks, pos_dict)

    def outputStream(self, networks, pos):
        """
        Creates a CX element generator added cartesianCoordinate from a list of igraph objects.

        :params networks: A list of igraph objects
        :params pos: postions of nodes
        :returns: A CX element generator
        """

        for i in IgraphAdapter.from_igraph(networks):
            yield i
        for k, v in pos.items():
            builder = NetworkElementBuilder('out_net')
            ele = builder.new_element()
            layout = ele.CartesianCoordinate
            layout.nodeId = k
            layout.x = v[0]
            layout.y = v[1]
            if len(v) == 3:
                # dim = 3
                layout.z = v[2]
            yield ele

if __name__ == "__main__":

    analyzer = IgLayoutService()
    logging.warn('Starting igraph analysis service...')
    analyzer.run()
