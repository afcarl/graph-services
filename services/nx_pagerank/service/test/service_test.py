import unittest
import networkx
import requests
import json
import logging
from cxmate import Adapter
from myservice import NxPagerankService

URL = 'http://localhost'
HEADERS = {'Content-type': 'application/json'}


class TestNxLayoutService(unittest.TestCase):

    def testNodePosition1(self, filename='../../sample-data/sample.cx', parameter=''):
        data = open(file=filename, mode='r')
        cx = json.load(data)
        data = open(file=filename, mode='r')
        node_list1, node_cnt1 = countNode(cx)
        r = requests.post(url=URL+parameter, headers=HEADERS, data=data)
        node_list2, node_cnt2 = countNodeAttribute(r.json()['data'], 'pagerank')

        self.assertEqual(node_cnt1, node_cnt2, msg='the number of node {} != {}'.format(node_cnt1, node_cnt2))

    def testNodePosition1_param(self):
        parameter = '?personalization=personalization&nstart=nstart&dangling=dangling&weight=weights'
        self.testNodePosition1(filename='../../sample-data/sample.cx', parameter=parameter)

    def testNodePosition2(self):
        self.testNodePosition1(filename='../../sample-data/sample2.cx', parameter='')

    def testNodePosition3(self):
        self.testNodePosition1(filename='../../sample-data/sample3.cx', parameter='')

    def testNodePositionEmptyNetwork(self):
        self.testNodePosition1(filename='../../sample-data/empty.cx')

    def testNodePositionOneNodeNetwork(self):
        self.testNodePosition1(filename='../../sample-data/1node.cx')


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


if __name__ == '__main__':
    unittest.main()
