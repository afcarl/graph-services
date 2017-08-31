import cxmate
import networkx
import logging
from directed_nx_adapter import DiAdapter


class MyService(cxmate.Service):

    def process(self, params, input_stream):
        for k, v in params.items():
            if v == 'None':
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
            pr = networkx.pagerank(net, **params)
            networkx.set_node_attributes(net, 'pagerank', pr)

        return DiAdapter.from_networkx(network)

if __name__ == "__main__":
    myService = MyService()
    myService.run()
