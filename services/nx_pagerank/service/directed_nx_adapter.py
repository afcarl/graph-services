import cxmate
from cxmate.service import Adapter
import networkx
import logging


class DiAdapter(cxmate.Adapter):
    """
    Static methods to convert directed networkX formats to and from CX stream iterators
    """

    @staticmethod
    def to_directed_networkx(ele_iter):
        """
        Creates a list of networkx objects by read network elements from ele_iter

        :param ele_iter: A CX element generator
        :returns: A list of networkx objects
        """
        networks = []
        while ele_iter:
            network, ele_iter = DiAdapter.read_directed_networkx(ele_iter)
            networks.append(network)
        return networks
       
    @staticmethod
    def read_directed_networkx(ele_iter):
        network = networkx.DiGraph()
        attrs = []
        edges = {}
        for ele in ele_iter:
            if not 'label' in network.graph:
                network.graph['label'] = ele.label
            if ele.label != network.graph['label']:
                return network, itertools.chain([ele], ele_iter)
            ele_type = ele.WhichOneof('element')
            if ele_type == 'node':
                node = ele.node
                network.add_node(int(node.id), name=node.name)
            elif ele_type == 'edge':
                edge = ele.edge
                src, tgt = int(edge.sourceId), int(edge.targetId)
                edges[int(edge.id)] = (src, tgt)
                network.add_edge(src, tgt, id=int(edge.id), interaction=edge.interaction)
            elif ele_type == 'nodeAttribute':
                attr = ele.nodeAttribute
                network.add_node(attr.nodeId, **{attr.name: Adapter.parse_value(attr)})
            elif ele_type == 'edgeAttribute':
                attr = ele.edgeAttribute
                attrs.append(attr)
            elif ele_type == 'networkAttribute':
                attr = ele.networkAttribute
                network.graph[attr.name] = Adapter.parse_value(attr)
            for attr in attrs:
                source, target = edges[int(attr.edgeId)]
                network[source][target][attr.name] = Adapter.parse_value(attr)
        return network, None
