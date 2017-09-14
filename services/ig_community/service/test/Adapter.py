import igraph as ig
import logging
import itertools
import cxmate
from cxmate.cxmate_pb2 import NetworkElement

logger = logging.getLogger('IgraphAdapter')
logger.setLevel(logging.INFO)


class IgraphAdapter(cxmate.Adapter):

    @staticmethod
    def to_igraph(ele_iter):
        networks = []
        while ele_iter:
            network, ele_iter = IgraphAdapter.read_igraph(ele_iter)
            networks.append(network)
        return networks

    @staticmethod
    def read_igraph(ele_iter):
        network = ig.Graph(directed=False)
        attrs = []
        nodes = {}
        edges = {}
        edges_index = {}
        for ele in ele_iter:
            if not 'label' in network.attributes():
                network['label'] = ele.label
            if ele.label != network['label']:
                return network, itertools.chain([ele], ele_iter)
            ele_type = ele.WhichOneof('element')
            if ele_type == 'node':
                node = ele.node
                network.add_vertex(name=node.name, nodeId=int(node.id))
                nodes[node.id] = network.vcount() - 1
            elif ele_type == 'edge':
                edge = ele.edge
                src, tgt = int(edge.sourceId), int(edge.targetId)
                # src_index = network.vs[nodes[src]].index
                # tgt_index = network.vs[nodes[tgt]].index
                src_index = nodes[src]
                tgt_index = nodes[tgt]
                edges[int(edge.id)] = (src_index, tgt_index)
                network.add_edge(src_index, tgt_index, id=int(edge.id), interaction=edge.interaction)
                edges_index[int(edge.id)] = network.ecount() - 1
            elif ele_type == 'nodeAttribute':
                attr = ele.nodeAttribute
                network.vs[nodes[attr.nodeId]][attr.name] = IgraphAdapter.parse_value(attr)
            elif ele_type == 'edgeAttribute':
                attr = ele.edgeAttribute
                attrs.append(attr)
            elif ele_type == 'networkAttribute':
                attr = ele.networkAttribute
                network[attr.name] = IgraphAdapter.parse_value(attr)
            for attr in attrs:
                source, target = edges[int(attr.edgeId)]
                network.es[edges_index[attr.edgeId]][attr.name] = IgraphAdapter.parse_value(attr)
                attrs = []
        return network, None

    @staticmethod
    def parse_value(attr):
        value = attr.value
        if attr.type:
            if attr.type in ('boolean'):
                value = value.lower() in ('true')
            elif attr.type in ('double', 'float'):
                value = float(value)
            elif attr.type in ('integer', 'short', 'long'):
                value = int(value)
        return value

    @staticmethod
    def from_igraph(networks):
        """
        Creates a CX element generator from a list of igraph objects

        :param networks: A list of igraph objects
        :returns: A CX element generator
        """

        for network in networks:
            builder = NetworkElementBuilder(network['label'])

            for node in network.vs():
                nodeId = node['nodeId']
                attrs = node.attributes()
                yield builder.Node(nodeId, str(attrs.get('name', '')))

                for k, v in attrs.items():
                    if k not in ('name', 'nodeId') and v is not None:
                        yield builder.NodeAttribute(nodeId, k, v)

            for edge in network.es():
                sourceId = network.vs[edge.source]['nodeId']
                targetId = network.vs[edge.target]['nodeId']
                attrs = edge.attributes()
                yield builder.Edge(attrs.get('id', edge.index), sourceId, targetId, attrs.get('interaction', ''))

                for k, v in attrs.items():
                    if k not in ('interaction', 'id') and v is not None:
                        yield builder.EdgeAttribute(attrs.get('id', edge.index), k, v)

            for attrs_key in network.attributes():
                yield builder.NetworkAttribute(attrs_key, network[attrs_key])


class NetworkElementBuilder():
    """
    Factory class for declaring the network element from igraph attributes
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
            return 'double', str(value)
        elif isinstance(value, int):
            return 'integer', str(value)
        return 'string', str(value)