import cxmate
import networkx
from networkx.drawing.nx_pydot import graphviz_layout
from cxmate.service import NetworkElementBuilder
import logging


class MyService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)

        network = cxmate.Adapter.to_networkx(input_stream)
        
        for net in network:
            net.graph['label'] = 'Output'
            net.graph['name'] = params['name']
        for n, nodedata in net.nodes_iter(data=True):
            if 'name' in nodedata.keys():
                del nodedata['name']
        pos = graphviz_layout(net, prog=params['prog'], root=params['root'])

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
