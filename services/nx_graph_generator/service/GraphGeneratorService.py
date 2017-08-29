import cxmate
import networkx


class GraphGeneratorService(cxmate.Service):
    def process(self, params, input_stream):
        """
        process is a required method, if it's not implemented, cxmate.service will throw an error
        this process implementation will echo the received network back to the sender

        :param input_stream: a python generator that returns CX elements
        :returns: a python generator that returns CX elements
        """
        # network = cxmate.Adapter.to_networkx(input_stream)
        network = self.generate_graph(params)
        cx = cxmate.Adapter.from_networkx(network)
        return cx

    def generate_graph(self, params):
        network = networkx.duplication_divergence_graph(params["n"],params["p"], params["seed"], params["directed"])

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

