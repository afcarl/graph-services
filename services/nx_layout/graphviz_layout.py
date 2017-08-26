import cxmate
import networkx.drawing as nx
from networkx.utils import open_file, make_str
from networkx.drawing.nx_agraph import graphviz_layout
from service import NetworkElementBuilder


class MyService(cxmate.Service):

    def process(self, params, input_stream):
        """
        process is a required method, if it's not implemented, cxmate.service will throw an error
        this process implementation will echo the received network back to the sender

        :param input_stream: a python generator that returns CX elements
        :returns: a python generator that returns CX elements
        """

        network = cxmate.Adapter.to_networkx(input_stream)

        for net in network:
            net.graph['label'] = 'Output'
            # prog
            # circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi
            pos = graphviz_layout(net, prog='circo')

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
    # run starts the service listening for requests from cxMate
    myService.run()
