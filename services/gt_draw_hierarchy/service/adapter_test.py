import unittest
import random

import graph_tool
from Adapter import GraphToolAdapter

class TestGraphToolAdapter(unittest.TestCase):
    def test_get_gt_type(self):
        self.assertEqual(GraphToolAdapter.get_gt_type(1), 'int')
        self.assertEqual(GraphToolAdapter.get_gt_type(1.0), 'float')
        self.assertEqual(GraphToolAdapter.get_gt_type(True), 'bool')
        self.assertEqual(GraphToolAdapter.get_gt_type("asdf"), 'string')
        self.assertEqual(GraphToolAdapter.get_gt_type({1:"asdf"}), 'object')
        self.assertEqual(GraphToolAdapter.get_gt_type([1]), 'vector<int>')
        self.assertEqual(GraphToolAdapter.get_gt_type([1.0]), 'vector<float>')
        self.assertEqual(GraphToolAdapter.get_gt_type([True]), 'vector<bool>')
        self.assertEqual(GraphToolAdapter.get_gt_type(["asdf"]), 'vector<string>')
        self.assertEqual(GraphToolAdapter.get_gt_type([{1:"asdf"}]), 'object')

    def test_from_graph_tool(self):
        net, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=50)
        net.gp.desc = net.new_gp("string")
        net.gp.desc = 'example'
        nodeCount = 0
        edgeCount = 0

        for aspect in GraphToolAdapter.from_graph_tool([net]):
            which = aspect.WhichOneof('element')
            if which == 'node':
                nodeCount += 1
                node = aspect.node
                self.assertEqual(net.vp['name'][net.vertex(node.id)], node.name)
            elif which == 'edge':
                edgeCount += 1
                edge = aspect.edge
                self.assertEqual(edge.id, net.ep.id[net.edge(edge.sourceId, edge.targetId)])
            elif which == 'nodeAttribute':
                attr = aspect.nodeAttribute
                self.assertEqual(net.vp[attr.name][net.vertex(node.id)], attr.value)
            elif which == 'edgeAttribute':
                attr = aspect.edgeAttribute
                a, b = edgeList[attr.edgeId]
                self.assertEqual(str(net.ep.value[net.edge(edge.sourceId, edge.targetId)]), attr.value)
            elif which == 'networkAttribute':
                attr = aspect.networkAttribute
                self.assertEqual(net.gp[attr.name], attr.value)
            else:
                print("UNTESTED %s" % aspect)
        self.assertEqual(nodeCount, len(net.get_vertices()))
        self.assertEqual(edgeCount, len(net.get_edges()))

    def test_to_graph_tool(self):
        net, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=50,
                data={'keyStr': 'value',
                'keyInt': 1,
                'keyFloat': 1.2,
                'keyBool': True})

        stream = GraphToolAdapter.from_graph_tool([net])
        net_res_list = GraphToolAdapter.to_graph_tool(stream)
        compare_graph_tool(net, net_res_list[0])
        self.assertEqual(net.gp.keys(), net_res_list[0].gp.keys())
        for k in net.gp.keys():
            self.assertEqual(net.gp[k], net_res_list[0].gp[k])

    def testUnusualAttributeType(self):
        net, edgeList = create_mock_graph_tool(num_nodes=100, num_edges=50, data={'keyDict': {1: 2}})
        stream = GraphToolAdapter.from_graph_tool([net])
        net_res_list = GraphToolAdapter.to_graph_tool(stream)
        compare_graph_tool(net, net_res_list[0])
        # autoconvert to string for unrecognized value types
        self.assertEqual(str(net.gp['keyDict']), net_res_list[0].gp['keyDict'])

    def testLargeNetwork(self):
        net, edgeList = create_mock_graph_tool(num_nodes=10000, num_edges=5000)
        stream = GraphToolAdapter.from_graph_tool([net])
        net_res_list = GraphToolAdapter.to_graph_tool(stream)
        compare_graph_tool(net, net_res_list[0])

    def testMultipleNetworks(self):
        nets = [create_mock_graph_tool('net1')[0], create_mock_graph_tool('net2')[0]]
        streams = GraphToolAdapter.from_graph_tool(nets)
        res_nets = GraphToolAdapter.to_graph_tool(streams)
        compare_graph_tool(nets[0], res_nets[0])
        compare_graph_tool(nets[1], res_nets[1])

def compare_graph_tool(net1, net2):
    """
    net1 is a graph-tool's Graph
    net2 is a graph-tool's Graph
    """
    for e1 in net1.edges():
        e2 = net2.edge(e1.source(), e1.target())
        val1 = net1.ep['value'][e1]
        val2 = net2.ep['value'][e2]
        assert val1 == val2, "Edge attribute incorrect. %s != %s" % (val1, val2)
    for n1 in net1.vertices():
        n2 = net2.vertex(int(n1))
        name1 = net1.vp['name'][n1]
        name2 = net2.vp['name'][n2]
        assert name1 == name2, "Node name incorrect. %s != %s" % (name1, name2)
    net1_graph = {k: (v if type(v) in (float, str, int, bool) else str(v)) for k, v in dict(net1.gp).items()}
    net2_graph = {k: (v if type(v) in (float, str, int, bool) else str(v)) for k, v in dict(net2.gp).items()}
    assert net1_graph == net2_graph, "Network attributes do not match. %s != %s" % (net1_graph, net2_graph)
    return True

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
        n.ep.value = n.new_ep(GraphToolAdapter.get_gt_type(val))
        n.ep.value[e] = val
        ID += 1
    for k, v in data.items():
        if k not in n.gp:
            n.gp[k] = n.new_gp(GraphToolAdapter.get_gt_type(v))
        n.gp[k] = v
    return n, edgeList

if __name__ == '__main__':
    unittest.main()