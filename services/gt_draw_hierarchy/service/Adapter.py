import cxmate
import itertools

from graph_tool import all as gt
from NetworkElementBuilder import NetworkElementBuilder

class GraphToolAdapter(cxmate.Adapter):
    def __init__(self, arg):
        super(GraphToolAdapter, self).__init__()
        
    @staticmethod
    def to_graph_tool(ele_iter):
        """
        Creates a list of graph-tool objects by read network elements from ele_iter

        :param ele_iter: A CX element generator
        :returns: A list of graph-tool objects
        """
        networks = []
        while ele_iter:
            network, ele_iter = GraphToolAdapter.read_graph_tool(ele_iter)
            networks.append(network)
        return networks

    @staticmethod
    def read_graph_tool(ele_iter):
        network = gt.Graph(directed=True)
        attrs = []
        edges = {}
        nodes = {}
        network.vp.id = network.new_vp("int")
        network.vp.name = network.new_vp("string")
        network.ep.id = network.new_ep("int")
        network.ep.interaction = network.new_ep("string")

        for ele in ele_iter:
            if not 'label' in network.graph_properties:
                network.graph_properties["label"] = network.new_graph_property("string")
                network.graph_properties["label"] = ele.label
            if ele.label != network.graph_properties['label']:
                return network, itertools.chain([ele], ele_iter)
            ele_type = ele.WhichOneof('element')
            if ele_type == 'node':
                node = ele.node
                new_node = network.add_vertex()
                nodes[node.id] = new_node
                network.vp.id[new_node] = int(node.id)
                network.vp.name[new_node] = node.name
            elif ele_type == 'edge':
                edge = ele.edge
                src, tgt = int(edge.sourceId), int(edge.targetId)
                new_edge = network.add_edge(nodes[src], nodes[tgt])
                edges[int(edge.id)] = new_edge
                network.ep.id[new_edge] = int(edge.id)
                network.ep.interaction[new_edge] = edge.interaction
            elif ele_type == 'nodeAttribute':
                attr = ele.nodeAttribute
                value = GraphToolAdapter.parse_value(attr)
                attr_type = GraphToolAdapter.get_gt_type(value)
                if attr.name not in network.vp:
                    network.vertex_properties[attr.name] = network.new_vertex_property(attr_type)
                network.vertex_properties[attr.name][nodes[attr.nodeId]] = value
            elif ele_type == 'edgeAttribute':
                attr = ele.edgeAttribute
                value = GraphToolAdapter.parse_value(attr)
                attr_type = GraphToolAdapter.get_gt_type(value)
                if attr.name not in network.ep:
                    network.ep[attr.name] = network.new_ep(attr_type)
                network.ep[attr.name][edges[attr.edgeId]] = value
            elif ele_type == 'networkAttribute':
                attr = ele.networkAttribute
                value = GraphToolAdapter.parse_value(attr)
                attr_type = GraphToolAdapter.get_gt_type(value)
                if attr.name not in network.gp:
                    network.gp[attr.name] = network.new_graph_property(attr_type)
                network.gp[attr.name] = value
        return network, None

    @staticmethod
    def get_gt_type(x, is_vector =  False):
        python_type = x.__class__.__name__

        gt_type = 'object'
        if   python_type == 'str':
            gt_type = 'string'
        elif python_type in ('int', 'float', 'bool'):
            gt_type = python_type
        elif python_type == 'list' and len(x) > 0:
            if is_vector == False:  # avoid nested vector type
                gt_type = GraphToolAdapter.get_gt_type(x[0], is_vector=True)
        if gt_type == 'object' and is_vector:
            return 'object'
        return gt_type if not is_vector else 'vector<{t}>'.format(t=gt_type)


    @staticmethod
    def from_graph_tool(networks, poss=None, only_layout=False):
        """
        Creates a CX element generator from a list of graph-tool objects

        :param networks: A list of graph-tool objects
        :returns: A CX element generator
        """

        def get_node_id(g, node):
            return g.vp.id[int(node)] if "id" in g.vp else int(node)

        for network, pos in itertools.zip_longest(networks, poss):
            graph_label = network.gp.label if "label" in network.gp else 'out_net'
            builder = NetworkElementBuilder(graph_label)
            edge_num = -1
            if only_layout:
                break

            for node in network.vertices():
                attrs = network.vp
                node_id = get_node_id(network, node)

                if 'name' not in attrs:
                    attrs.name = network.new_vp('string')  # make sure name exists
                yield builder.Node(node_id, attrs.name[node])

                for attr_name, pmap in attrs.items():
                    if attr_name not in ('name', 'id'):
                        yield builder.NodeAttribute(node_id, attr_name, pmap[node])

            for edge in network.edges():
                source_node, target_node = edge.source(), edge.target()
                edge_num += 1
                attrs = network.ep
                sourceId = get_node_id(network, source_node)
                targetId = get_node_id(network, target_node)
                edge_id = attrs.id[edge] if "id" in attrs else edge_num

                if 'interaction' not in attrs:
                    attrs.interaction = network.new_ep('string')  # make sure interaction exists
                yield builder.Edge(edge_id, sourceId, targetId, attrs.interaction[edge])

                for attr_name, pmap in attrs.items():
                    if attr_name not in ('interaction', 'id'):
                        yield builder.EdgeAttribute(edge_id, attr_name, pmap[edge])

            for k in network.gp.keys():
                yield builder.NetworkAttribute(k, network.gp[k])

        if pos:
            for node in network.vertices():
                position = pos[node]
                yield builder.Position(position, get_node_id(network, node))
