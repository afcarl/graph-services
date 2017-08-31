import cxmate
import networkx
from networkx.drawing.nx_pydot import graphviz_layout
from cxmate.service import NetworkElementBuilder
import logging


class MyService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)

        network = cxmate.Adapter.to_networkx(input_stream)

        nodedata_tmp = []        
        for net in network:
            net.graph['label'] = 'Output'
        for n, nodedata in net.nodes_iter(data=True):
            if 'name' in nodedata.keys():
                nodedata_tmp.append(nodedata['name'])
                del nodedata['name']
        pos = graphviz_layout(net, prog=params['prog'], root=params['root'])

        i = 0
        for n, nodedata in net.nodes_iter(data=True):
            nodedata['name'] = nodedata_tmp[i]
            i += 1

        return self.outputStream(network, pos)

    def outputStream(self, network, pos):
        for i in cxmate.Adapter.from_networkx(network):
            yield i
        for key in pos.keys():
            builder = NetworkElementBuilder('Output')
            ele = builder.new_element()
            layout = ele.CartesianCoordinate
            layout.nodeId = key
            layout.x = pos[key][0]
            layout.y = pos[key][1]
            yield ele


if __name__ == "__main__":
    myService = MyService()
    myService.run()
