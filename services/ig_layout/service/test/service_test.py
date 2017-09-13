import unittest
import networkx
import requests
import json
import logging
from cxmate import Adapter
from myservice import IgLayoutService

URL = 'http://localhost:3000'
HEADERS = {'Content-type': 'application/json'}


class TestIgLayoutService(unittest.TestCase):

    def testNodePosition1(self, filename='../../sample-data/sample.cx', parameter='', layout=''):
        data = open(file=filename, mode='r')
        cx = json.load(data)
        data = open(file=filename, mode='r')
        node_list1, node_cnt1 = countNode(cx)
        r = requests.post(url=URL+parameter, headers=HEADERS, data=data)

        node_list2, node_cnt2 = countcartesianLayout(r.json()['data'])

        self.assertEqual(node_cnt1, node_cnt2, msg='the number of node {} != {} in using algorithm {}'.format(node_cnt1, node_cnt2, layout))

        pos_set = []
        for node in node_list2.values():
            pos_set.append((node['x'], node['y'], node['z']))
        self.assertEqual(len(set(pos_set)), node_cnt2, msg='There are nodes with the same position, in using algorithm {}'.format(parameter))

    def testDefaultPrameters(self, filename='../../sample-data/sample.cx'):
        layout = [
            'bipartite&types=fixed',
            'circle',
            'drl',
            'fruchterman_reingold',
            'graphopt',
            'grid',
            'kamada_kawai',
            'lgl',
            'random',
            'star'
            ]

        for l in layout:
            parameter = '?layout={}'.format(l)
            self.testNodePosition1(filename=filename, parameter=parameter, layout=l)

    def testEmptyNetworkDefaultParameters(self):
        self.testDefaultPrameters(filename='../../sample-data/sample.cx')

    def testOneNodeNetworkDefaultParameters(self):
        self.testDefaultPrameters(filename='../../sample-data/1node.cx')


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


def countNodeAttribute(cx, name):
    node_list = {}
    for aspect in cx:
        for key, values in aspect.items():
            if "nodeAttributes" == key:
                for node in values:
                    if node['n'] == name:
                        node_list[node['po']] = node['v']
                        break

    return node_list, len(node_list)


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
