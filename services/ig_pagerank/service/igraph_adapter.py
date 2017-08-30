import igraph as ig
import logging

logger = logging.getLogger('igraph_adapter')
logger.setLevel(logging.INFO)


class IgraphAdapter():

    @staticmethod
    def to_igraph(input_stream):

        # Create an igraph object

        g = ig.Graph()

        node_dict = {}
        node_idx = 0
        edges = []

        for net_element in input_stream:
            net_element_type = net_element.WhichOneof('element')

            if net_element_type == 'node':

                node_id = int(net_element.node.id)

                node_dict[node_id] = node_idx
                node_idx += 1

                g.add_vertex(name=node_id)

            elif net_element_type == 'edge':
                edge = net_element.edge
                source_id = int(edge.sourceId)
                target_id = int(edge.targetId)
                edges.append((source_id, target_id))

        for e in edges:
            g.add_edge(node_dict[e[0]], node_dict[e[1]])

        logger.info(g.summary())

        return g
