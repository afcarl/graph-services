import unittest
import random
from collections import defaultdict

import graph_tool
from Adapter import GraphToolAdapter
from service import GtLayoutService

class TestGraphToolAdapter(unittest.TestCase):
    def test_all_nodes_have_layout(self):
        net1, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=300)
        GLS = GtLayoutService()
        params = {'layout-name': 'default', 'only-layout': True, 'root': 0, 'vweight': 'vweight', 'eweight': 'eweight', 'pin': 'pin', 'groups': 'groups', 'pos': 'pos', 'weight': 'weight', 'rel_order': 'rel_order', 'node_weight': 'node_weight'}

        gs, poss = GLS.process_graphs(params, [net1])
        cx = GraphToolAdapter.from_graph_tool(gs,  poss)
        b, ns, ls = has_corresponding_layout(cx)
        assert b, "Set of Node id and Set of Layout are different. <node %s> != <layout %s>" % (ns, ls)


    def test_all_algorithms(self):
        net1, edgeList = create_mock_planar(dim=[10, 15])
        GLS = GtLayoutService()
        params = {'layout-name': 'default', 'only-layout': True, 'root': 10, 'vweight': 'vweight', 'eweight': 'eweight', 'pin': 'pin', 'groups': 'groups', 'pos': 'pos', 'weight': 'weight', 'rel_order': 'rel_order', 'node_weight': 'node_weight'}

        layout_names = ["sfdp_layout", "fruchterman_reingold_layout", "arf_layout", "radial_tree_layout", "planar_layout", "random_layout"]
        # layout_names = ["sfdp_layout", "fruchterman_reingold_layout", "arf_layout", "radial_tree_layout", "random_layout"]
        for l in layout_names:
            params['layout-name'] = l
            gs, poss = GLS.process_graphs(params, [net1])
            cx = GraphToolAdapter.from_graph_tool(gs,  poss)
            b, ns, ls = has_corresponding_layout(cx)
            assert b, "Set of Node id and Set of Layout are different. Algorithm: %s <node %s> != <layout %s>" % (l, ns, ls)

    def test_nodes_have_unique_position(self):
        net1, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=300)
        GLS = GtLayoutService()
        params = {'layout-name': 'default', 'only-layout': True, 'root': 0, 'vweight': 'vweight', 'eweight': 'eweight', 'pin': 'pin', 'groups': 'groups', 'pos': 'pos', 'weight': 'weight', 'rel_order': 'rel_order', 'node_weight': 'node_weight'}

        gs, poss = GLS.process_graphs(params, [net1])
        cx = GraphToolAdapter.from_graph_tool(gs,  poss)
        b, dp = has_unique_position(cx)
        assert b, "There are same position nodes.  %s" % (dp)

    def test_with_parameter(self):
        net1, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=300)
        GLS = GtLayoutService()
        params = {'layout-name': 'default', 'only-layout': True, 'root': 0, 'vweight': 'vweight', 'eweight': 'eweight', 'pin': 'pin', 'groups': 'groups', 'pos': 'pos', 'weight': 'weight', 'rel_order': 'rel_order', 'node_weight': 'node_weight'}

        params["vweight"] = "vw"
        params["eweight"] = "ew"
        net1.vp.vw = net1.new_vp("int")
        net1.ep.ew = net1.new_ep("int")
        for v in net1.vertices():
            net1.vp.vw[v] = random.randint(0, 100)
        for edge in net1.edges():
            net1.ep.ew[edge] = random.randint(0, 100)
        gs, poss = GLS.process_graphs(params, [net1])
        cx = GraphToolAdapter.from_graph_tool(gs,  poss)
        b, dp = has_unique_position(cx)
        assert b, "There are same position nodes.  %s" % (dp)
        b, ns, ls = has_corresponding_layout(cx)
        assert b, "Set of Node id and Set of Layout are different. <node %s> != <layout %s>" % (ns, ls)


def has_corresponding_layout(cx):
    """
    params: cx generator
    returns: A boolean which indicates whether set of node id and set of layout id are identical or not.
    returns: 2 sets
    """
    node_set = set()
    layout_set = set()
    for aspect in cx:
        which = aspect.WhichOneof('element')
        if which == 'node':
            node = aspect.node
            node_set.add(node.id)
        elif which == 'CartesianCoordinate':
            layout = aspect.CartesianCoordinate
            layout_set.add(layout.nodeId)
    return node_set == layout_set, node_set - layout_set, layout_set - node_set
    # assert node_set == layout_set, "Set of Node id and Set of Layout are different. <node %s> != <layout %s>" % (node_set, layout_set)

def has_unique_position(cx):
    """
    params: cx generator
    returns: A boolean which indicates whether all nodes have unique position
    returns: 2 dict: key=position, value=node id set
    """
    pos_dict = defaultdict(set)  # key: position, value: nodeId set
    duplicate_positions = {}

    for aspect in cx:
        which = aspect.WhichOneof('element')
        if which == 'CartesianCoordinate':
            layout = aspect.CartesianCoordinate
            node_id = layout.nodeId
            x = layout.x
            y = layout.y
            p = "x:{x}, y:{y}".format(x=x, y=y)
            pos_dict[p].add(node_id)
    duplicate_positions = {p: s for p, s in pos_dict.items() if len(s) > 1}
    return not duplicate_positions, duplicate_positions


def create_mock_graph_tool(label='network_label', num_nodes=100, num_edges=100, data={}):
    edgeList = {}
    n = graph_tool.Graph()
    n.gp.label = n.new_gp("string")
    n.gp.label = label
    n.vp.name = n.new_vp("string")
    n.ep.id = n.new_ep("int")
    for n_id in range(num_nodes):
        v = n.add_vertex()
        n.vp.name[v] = hex(n_id)
    ID = num_nodes
    for e_id in range(num_edges):
        n1 = random.randint(0, num_nodes-1)
        n2 = random.randint(0, num_nodes-2)
        val = random.choice([1, 1.5, 'a', True])
        edgeList[ID] = (n1, n2)
        e = n.add_edge(n.vertex(n1), n.vertex(n2))
        n.ep.id[e] = ID
        n.ep.value = n.new_ep(GraphToolAdapter.get_gt_type(val))  # TODO: avoid destructive assiginment
        n.ep.value[e] = val
        ID += 1
    for k, v in data.items():
        if k not in n.gp:
            n.gp[k] = n.new_gp(GraphToolAdapter.get_gt_type(v))
        n.gp[k] = v
    return n, edgeList

def create_mock_planar(label='network_label', dim=[10 ,10], data={}):
    edgeList = {}
    n = graph_tool.generation.lattice(dim)
    n.gp.label = n.new_gp("string")
    n.gp.label = label
    n.vp.name = n.new_vp("string")
    n.ep.id = n.new_ep("int")
    ID = 0
    for v in n.vertices():
        n.vp.name[v] = hex(ID)
        ID += 1
    for edge in n.edges():
        source_node, target_node = edge.source(), edge.target()
        edgeList[ID] = (int(source_node), int(target_node))
        ID += 1
    for k, v in data.items():
        if k not in n.gp:
            n.gp[k] = n.new_gp(GraphToolAdapter.get_gt_type(v))
        n.gp[k] = v
    return n, edgeList

if __name__ == '__main__':
    unittest.main()