import cxmate
import logging
import igraph as ig
from Adapter import NetworkElementBuilder, IgraphAdapter

logger = logging.getLogger('igraph_service')
logger.setLevel(logging.INFO)


class IgStatisticsService(cxmate.Service):

    def process(self, params, input_stream):
        logging.warn(params)
        for k, v in params.items():
            if v == 'None':
                params[k] = None

        ig_networks = IgraphAdapter.to_igraph(input_stream)

        for net in ig_networks:
            net['label'] = 'out_net'
      
            if params['type'] == 'label_propagation':
                del params['type']
                cluster = net.community_label_propagation(**params)
                net.vs['cluster'] = cluster.membership
            elif params['type'] == 'optimal_modularity':
                cluster = net.community_optimal_modularity(weights=params['weights'])
                net.vs['cluster'] = cluster.membership
                net['modularity'] = cluster.modularity

        return IgraphAdapter.from_igraph(ig_networks)


if __name__ == "__main__":

    analyzer = IgStatisticsService()
    logging.warn('Starting igraph analysis service...')
    analyzer.run()
