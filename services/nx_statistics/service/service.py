import networkx as nx
import cxmate
import logging


class NetworkStatisticsService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)

        # Get the type of the analysis
        stat_type = params['type']


        networks = cxmate.Adapter.to_networkx(input_stream)

        for net in networks:
            # Calculate some statistics of the graph
            net.graph['label'] = 'out_net'
            stat = self.__get_stat(net, stat_type)
            nx.set_node_attributes(net, stat_type, stat)

        return cxmate.Adapter.from_networkx(networks)


    def __get_stat(self, net, stat_type):
        if stat_type is 'degree':
            return nx.degree_centrality(net)
        elif stat_type is 'closeness':
            return nx.closeness_centrality(net)
        else:
            return nx.betweenness_centrality(net)


if __name__ == "__main__":

    analyzer = NetworkStatisticsService()
    logging.warn('Starting graph analysis service...')
    analyzer.run()
