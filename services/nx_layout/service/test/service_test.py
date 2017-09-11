import unittest
import networkx
import requests
import json
import logging
from cxmate import Adapter
from myservice import NxLayoutService

URL = 'http://localhost'
HEADERS = {'Content-type': 'application/json'}


class TestNxLayoutService(unittest.TestCase):

    def testNodePosition1(self, filename='../../sample-data/sample.cx', parameter=''):
        data = open(file=filename, mode='r')
        cx = json.load(data)
        data = open(file=filename, mode='r')
        node_list1, node_cnt1 = countNode(cx)
        r = requests.post(url=URL+parameter, headers=HEADERS, data=data)
        node_list2, node_cnt2 = countcartesianLayout(r.json()['data'])

        self.assertEqual(node_cnt1, node_cnt2, msg='the number of node {} != {}'.format(node_cnt1, node_cnt2))

        for k1, node1 in node_list2.items():
            pos1 = (node1['x'], node1['y'], node1['z'])
            for k2, node2 in node_list2.items():
                pos2 = (node2['x'], node2['y'], node2['z'])
                if k1 != k2:
                    self.assertNotEqual(pos1, pos2, msg='the position of node {} == {}'.format(pos1, pos2))

    def testNodePosition1_dot(self):
        self.testNodePosition1(filename='../../sample-data/sample.cx', parameter='?prog=dot')

    def testNodePosition1_fdp(self):
        self.testNodePosition1(filename='../../sample-data/sample.cx', parameter='?prog=fdp')

    def testNodePosition1_circo(self):
        self.testNodePosition1(filename='../../sample-data/sample.cx', parameter='?prog=circo')

    def testNodePosition2_twopi(self):
        self.testNodePosition1(filename='../../sample-data/sample2.cx', parameter='?prog=twopi')

    def testNodePosition3(self):
        self.testNodePosition1(filename='../../sample-data/sample3.cx')
        

def countNode(cx):
    node_list = {}
    for aspect in cx:
        for key, values in aspect.items():
            if "nodes" == key:
                for node in values:
                    node_list[node['@id']] = node
    return node_list, len(node_list)


def countEdge(cx):
    edge_list = {}
    for aspect in cx:
        for key, values in aspect.items():
            if "edges" == key:
                for edge in values:
                    edge_list[edge['@id']] = edge
    return edge_list, len(edge_list)


def countcartesianLayout(cx):
    node_list = {}
    for aspect in cx:
        for key, values in aspect.items():
            if "cartesianLayout" == key:
                for node in values:
                    node_list[node['node']] = node
    return node_list, len(node_list)


if __name__ == '__main__':
    unittest.main()
