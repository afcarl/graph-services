import cxmate
import networkx
from pdb import set_trace as ps


class GraphGeneratorService(cxmate.Service):
    def process(self, params, input_stream):
        """
        process is a required method, if it's not implemented, cxmate.service will throw an error
        this process implementation will echo the received network back to the sender

        :param input_stream: a python generator that returns CX elements
        :returns: a python generator that returns CX elements
        """
        # network = cxmate.Adapter.to_networkx(input_stream)
        network = generate_graph()
        # for n in network:
            # ps()
        cx = cxmate.Adapter.from_networkx(network)
        return cx


def generate_graph():
    network = networkx.complete_graph(4)
    # network.remove_node(0)
    # ps()

    # this network doesn't have enough attributes to use cxmate.Adapter.from_networkx
    network.graph["label"] = "My output network"
    for n in network.nodes():
        network.node[n]["id"] = n
    for i, e in enumerate(network.edges()):
        s, t = e[0], e[1]
        network[s][t]["id"] = i
    yield network


if __name__ == "__main__":
  myService = GraphGeneratorService()
  myService.run() #run starts the service listening for requests from cxMate

