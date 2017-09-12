import unittest
import networkx
import requests
import json
import logging
from cxmate import Adapter
from myservice import IgCommunityDetectionService

URL = 'http://localhost'
HEADERS = {'Content-type': 'application/json'}


class TestIgCommunityDetectionService(unittest.TestCase):

    def testCommunityDetection1(self, filename='../../sample-data/sample.cx', parameter='?type=label_propagation'):
        data = open(file=filename, mode='r')
        cx = json.load(data)
        data = open(file=filename, mode='r')
        node_list1, node_cnt1 = countNode(cx)
        r = requests.post(url=URL+parameter, headers=HEADERS, data=data)
        node_list2, node_cnt2 = countNodeAttribute(r.json()['data'], 'community')
        node_list3, node_cnt3 = countNodeAttribute(r.json()['data'], 'community.color')

        self.assertEqual(node_cnt1, node_cnt2, msg='the number of node before service and node attributes (community) after {} != {}'.format(node_cnt1, node_cnt2))
        self.assertEqual(node_cnt1, node_cnt3, msg='the number of node before service and node attributes (color code) after {} != {}'.format(node_cnt1, node_cnt3))
        self.assertEqual(node_cnt2, node_cnt3, msg='the number of node attributes (community and color code) {} != {}'.format(node_cnt2, node_cnt3))
        self.assertEqual(len(set(node_list2.values())), len(set(node_list3.values())), msg='the number of community (community and color code) {} != {}'.format(len(set(node_list2)), len(set(node_list3))))

    def testCommunityDetection2(self):
        parameter = '?type=label_propagation&weight=weights&initial=initial&fixed=fixed'
        self.testCommunityDetection1(filename='../../sample-data/sample.cx', parameter=parameter)

    def testCommunityDetection3(self):
        parameter = '?type=fastgreedy'
        self.testCommunityDetection1(filename='../../sample-data/sample2.cx', parameter=parameter)

    def testCommunityDetection4(self):
        parameter = '?type=leading_eigenvector&clusters=7'
        self.testCommunityDetection1(filename='../../sample-data/sample2.cx', parameter=parameter)

    def testCommunityDetection5(self):
        parameter = '?type=edge_betweenness&clusters=4'
        self.testCommunityDetection1(filename='../../sample-data/sample2.cx', parameter=parameter)

    def testCommunityDetectionLargeNetwork6(self):
        parameter = ''
        self.testCommunityDetection1(filename='../../sample-data/sample3.cx', parameter=parameter)

    def testEmptyGraph(self):
        parameter = ''
        self.testCommunityDetection1(filename='../../sample-data/empty.cx', parameter=parameter)

    def testOneNodeGraph(self):
        parameter = ''
        self.testCommunityDetection1(filename='../../sample-data/1node.cx', parameter=parameter)


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
