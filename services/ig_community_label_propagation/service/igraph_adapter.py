import igraph as ig
import logging
from cxmate.cxmate_pb2 import *
from cxmate.cxmate_pb2_grpc import *

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

    @staticmethod
    def from_igraph(network):
        """
        Creates a CX element generator from a list of igraph objects

        :param networks: A list of igraph objects
        :returns: A CX element generator
        """

    # for network in networks:
        builder = NetworkElementBuilder(network['label'])

        for node in network.vs():
            nodeId = node.index
            attrs = node.attributes()
            yield builder.Node(nodeId, str(attrs.get('name', '')))

            for k, v in attrs.items():
                if k not in ('name'):
                    yield builder.NodeAttribute(nodeId, k, v)

        for edge in network.es():
            sourceId = edge.source
            targetId = edge.target
            attrs = edge.attributes()
            yield builder.Edge(attrs.get('id', edge.index), sourceId, targetId, attrs.get('interaction', ''))

            for k, v in attrs.items():
                if k not in ('interaction', 'id'):
                    yield builder.EdgeAttribute(attrs.get('id', edge.index), k, v)

        for attrs_key in network.attributes():
            yield builder.NetworkAttribute(attrs_key, network[attrs_key])


class NetworkElementBuilder():
    """
    Factory class for declaring the network element from igraph attributes
    (should import this class from service.py and not write here?)
    """

    def __init__(self, label):
        self.label = label

    def Node(self, nodeId, name):
        ele = self.new_element()
        node = ele.node
        node.id = nodeId
        node.name = name
        return ele

    def Edge(self, edgeId, sourceId, targetId, interaction):
        ele = self.new_element()
        edge = ele.edge
        edge.id = edgeId
        edge.sourceId = sourceId
        edge.targetId = targetId
        edge.interaction = interaction
        return ele

    def NodeAttribute(self, nodeId, key, value):
        ele = self.new_element()
        nodeAttr = ele.nodeAttribute
        nodeAttr.nodeId = nodeId
        typ, value = self.from_value(value)
        nodeAttr.type = typ
        nodeAttr.name = key
        nodeAttr.value = value
        return ele

    def EdgeAttribute(self, edgeId, key, value):
        ele = self.new_element()
        edgeAttr = ele.edgeAttribute
        edgeAttr.edgeId = edgeId
        typ, value = self.from_value(value)
        edgeAttr.type = typ
        edgeAttr.name = key
        edgeAttr.value = value
        return ele

    def NetworkAttribute(self, key, value):
        ele = self.new_element()
        networkAttr = ele.networkAttribute
        networkAttr.name = key
        typ, value = self.from_value(value)
        networkAttr.type = typ
        networkAttr.value = value
        return ele

    def new_element(self):
        ele = NetworkElement()
        ele.label = self.label
        return ele

    def from_value(self, value):
        if isinstance(value, bool):
            return 'boolean', str(value)
        elif isinstance(value, float):
            return 'float', str(value)
        elif isinstance(value, int):
            return 'integer', str(value)
        return 'string', str(value)