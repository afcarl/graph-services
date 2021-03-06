import cxmate
import networkx
import logging
from directed_nx_adapter import DiAdapter


class NxPagerankService(cxmate.Service):

    def process(self, params, input_stream):
        """
        CI service for creating node positions for the given network data using Graphviz.
        """
        for k, v in params.items():
            if v == str(None):
                params[k] = None

        logging.warn(params)

        if params['is_directed']:
            # network is directed graph
            network = DiAdapter.to_directed_networkx(input_stream)
        else:
            # network is non-directed graph
            network = DiAdapter.to_networkx(input_stream)
        del params['is_directed']

        for net in network:
            net.graph['label'] = 'Output'

            dict_parameters = ['personalization', 'dangling', 'nstart']
            for parameter in dict_parameters:
                # dict_parameters can be used the name of nodeAttribute
                if params[parameter] is not None:
                    params[parameter] = networkx.get_node_attributes(net, params[parameter])

            pr = networkx.pagerank(net, **params)
            networkx.set_node_attributes(net, 'pagerank', pr)

        return DiAdapter.from_networkx(network)


if __name__ == "__main__":
    myService = NxPagerankService()
    myService.run()
