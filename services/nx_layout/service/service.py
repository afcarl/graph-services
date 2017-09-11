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

        # Replace string None to Python None data type
        for k, v in params.items():
            if v == str(None):
                params[k] = None

        networks = cxmate.Adapter.to_networkx(input_stream)
        nodedata_tmp = []

        # For now, this service supports for single-graph only.
        net = networks[0]

        net.graph['label'] = OUTPUT_LABEL
        if params['prog'] == 'twopi' and 'root' in net.graph.keys():
            # When 'twopi' is selected in parameter 'prog', root node is used 'root' in NetworkAttributes
            params['root'] = net.graph['root']
        for n, nodedata in net.nodes_iter(data=True):
            # Prevent duplication of attribute 'name'.
            if 'name' in nodedata.keys():
                nodedata_tmp.append(nodedata['name'])
                del nodedata['name']
        logging.debug(params)
        pos = graphviz_layout(net, **params)

        # Set removed attribute 'name' again.
        i = 0
        for n, nodedata in net.nodes_iter(data=True):
            nodedata['name'] = nodedata_tmp[i]
            i += 1

        return self.outputStream([net], pos)

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
