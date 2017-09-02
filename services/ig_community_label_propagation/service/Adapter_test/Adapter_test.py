import unittest
import random
import logging
import igraph
from Adapter import IgraphAdapter, NetworkElementBuilder


class TestIgraphAdapter(unittest.TestCase):

    def testFromValue(self):
        builder = NetworkElementBuilder('test')
        typ, value = builder.from_value(1)
        self.assertEqual(typ, 'integer')
        self.assertEqual(value, '1')

        typ, value = builder.from_value(False)
        self.assertEqual(typ, 'boolean')
        self.assertEqual(value, 'False')

        typ, value = builder.from_value(1.5)
        self.assertEqual(typ, 'double')
        self.assertEqual(value, '1.5')

        typ, value = builder.from_value('H')
        self.assertEqual(typ, 'string')
        self.assertEqual(value, 'H')

        typ, value = builder.from_value({1: 2})
        self.assertEqual(typ, 'string')
        self.assertEqual(value, '{1: 2}')

    def test_from_igraph(self):
        net, edgeList = create_mock_igraph(num_nodes=100, num_edges=50)
        net['desc'] = 'example'
        nodeCount = 0
        edgeCount = 0
        for aspect in IgraphAdapter.from_igraph([net]):
            which = aspect.WhichOneof('element')
            if which == 'node':
                nodeCount += 1
                node = aspect.node
                self.assertEqual(net.vs[node.id]['name'], node.name)
            elif which == 'edge':
                edgeCount += 1
                edge = aspect.edge
                self.assertEqual(edge.id, net.es.find(id=edge.id)['id'])
            elif which == 'nodeAttribute':
                attr = aspect.nodeAttribute
                self.assertEqual(net.vs[attr.nodeId][attr.name], attr.value)
            elif which == 'edgeAttribute':
                attr = aspect.edgeAttribute
                a, b = edgeList[attr.edgeId]
                self.assertEqual(str(net.es.find(id=attr.edgeId)['value']), attr.value)
            elif which == 'networkAttribute':
                attr = aspect.networkAttribute
                self.assertEqual(net[attr.name], attr.value)
            else:
                print("UNTESTED %s" % aspect)
        self.assertEqual(nodeCount, net.vcount())
        self.assertEqual(edgeCount, net.ecount())

    def test_to_igraph(self):
        net, edgeList = create_mock_igraph(num_nodes=100, num_edges=50,
                                           data={'keyStr': 'value',
                                                 'keyInt': 1,
                                                 'keyFloat': 1.2,
                                                 'keyBool': True})
      
        stream = IgraphAdapter.from_igraph([net])
        net_res_list = IgraphAdapter.to_igraph(stream)
        compare_igraph(net, net_res_list[0])
        net_graph = {k: (net[k] if type(net[k]) in (float, str, int, bool) else str(net[k])) for k in net.attributes()}
        net_res_graph = {k: (net_res_list[0][k] if type(net_res_list[0][k]) in (float, str, int, bool) else str(net_res_list[0][k])) for k in net_res_list[0].attributes()}
        self.assertEqual(net_graph, net_res_graph)

    def testUnusualAttributeType(self):
        net, edgeList = create_mock_igraph(num_nodes=100, num_edges=50, data={'keyDict': {1: 2}})
        stream = IgraphAdapter.from_igraph([net])
        net_res_list = IgraphAdapter.to_igraph(stream)
        compare_igraph(net, net_res_list[0])
        # autoconvert to string for unrecognized value types
        self.assertEqual(str(net['keyDict']), net_res_list[0]['keyDict'])

    def testLargeNetwork(self):
        net, edgeList = create_mock_igraph(num_nodes=10000, num_edges=5000)
        stream = IgraphAdapter.from_igraph([net])
        net_res_list = IgraphAdapter.to_igraph(stream)
        compare_igraph(net, net_res_list[0])

    def testMultipleNetworks(self):
        nets = [create_mock_igraph('net1')[0], create_mock_igraph('net2')[0]]
        streams = IgraphAdapter.from_igraph(nets)
        res_nets = IgraphAdapter.to_igraph(streams)
        compare_igraph(nets[0], res_nets[0])
        compare_igraph(nets[1], res_nets[1])


def compare_igraph(net1, net2):
    for eg in net1.es():
        a = eg.source
        b = eg.target
        id = eg['id']
        val = net2.es.find(_source=a, _target=b, id=id)['value']
        assert val == net1.es.find(_source=a, _target=b, id=id)['value'], "Edge attribute incorrect. %s != %s [a:%s,b:%s,id:%s]" % (val, net1.es.find(_source=a, _target=b, id=id)['value'], a, b, id)
    for vertex in net1.vs():
        assert vertex['name'] == net2.vs[vertex.index]['name'], "Node name incorrect. %s != %s" % (attr['name'], net2.vs[vertex.index]['name'])
    net1_graph = {k: (net1[k] if type(net1[k]) in (float, str, int, bool) else str(net1[k])) for k in net1.attributes()}
    net2_graph = {k: (net2[k] if type(net2[k]) in (float, str, int, bool) else str(net2[k])) for k in net2.attributes()}
    assert net1_graph == net2_graph, "Network attributes do not match. %s != %s" % (net1_graph, net2_graph)
    return True


def create_mock_igraph(label='network_label', num_nodes=100, num_edges=100, data={}):
    edgeList = {}
    n = igraph.Graph(directed=False)
    n['label'] = label
    for n_id in range(num_nodes):
        n.add_vertex(name=hex(n_id), nodeId=n_id)
    ID = num_nodes
    for e_id in range(num_edges):
        n1 = random.randint(0, num_nodes-1)
        n2 = random.randint(0, num_nodes-2)
        val = random.choice([1, 1.5, 'a', True])
        edgeList[ID] = (n1, n2)
        n.add_edge(n1, n2, id=ID, value=val)
        ID += 1
    for k, v in data.items():
        n[k] = v
    return n, edgeList

if __name__ == '__main__':
    unittest.main()
