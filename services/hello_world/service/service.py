import networkx as nx
import cxmate
import logging


class HelloService(cxmate.Service):
    def process(self, params, input_stream):
        logging.warn(params)

        networks = cxmate.Adapter.to_networkx(input_stream)

        for net in networks:
            # Calculate some statistics of the graph
            net.graph['label'] = 'out_net'
            net.graph['name'] = params['name']
            net.graph['density'] = nx.density(net)
            net.graph['average_clustering'] = nx.average_clustering(net)

        return cxmate.Adapter.from_networkx(networks)


if __name__ == "__main__":
    my_service = HelloService()
    logging.warn('Starting service...')
    my_service.run()
