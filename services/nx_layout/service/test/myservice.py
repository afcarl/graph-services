import cxmate
from networkx.drawing.nx_pydot import graphviz_layout
from cxmate.service import NetworkElementBuilder
import logging

logging.basicConfig(level=logging.DEBUG)

# Label for CXmate output
OUTPUT_LABEL = 'out_net'


class NxLayoutService(cxmate.Service):

    def process(self, params, input_stream):
        """
        CI service for creating node positions for the given network data using Graphviz.
        """

        logging.debug(params)

        # Replace string None to Python None data type
        for k, v in params.items():
            if v == str(None):
                params[k] = None

        networks = cxmate.Adapter.to_networkx(input_stream)
        nodedata_tmp = []

        for net in networks:
            net.graph['label'] = OUTPUT_LABEL
            for n, nodedata in net.nodes_iter(data=True):
                # Prevent duplication of attribute 'name'.
                if 'name' in nodedata.keys():
                    nodedata_tmp.append(nodedata['name'])
                    del nodedata['name']
            pos = graphviz_layout(net, **params)

            # Set removed attribute 'name' again.
            i = 0
            for n, nodedata in net.nodes_iter(data=True):
                nodedata['name'] = nodedata_tmp[i]
                i += 1

        return self.outputStream(networks, pos)

    def outputStream(self, networks, pos):
        """
        Creates a CX element generator added cartesianCoordinate from a list of networkx objects.

        :params networks: A list of networkX objects
        :params pos: postions of nodes
        :returns: A CX element generator
        """

        for i in cxmate.Adapter.from_networkx(networks):
            yield i
        for key in pos.keys():
            # Make new element CartesianCoordinate
            builder = NetworkElementBuilder(OUTPUT_LABEL)
            ele = builder.new_element()
            layout = ele.CartesianCoordinate
            layout.nodeId = key
            layout.x = pos[key][0]
            layout.y = pos[key][1]
            yield ele


if __name__ == "__main__":
    layout = NxLayoutService()
    logging.info('Starting networkx layout service...')
    layout.run()
