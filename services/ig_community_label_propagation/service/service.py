import cxmate
import logging
import igraph as ig
from Adapter import NetworkElementBuilder, IgraphAdapter

logger = logging.getLogger('igraph_service')
logger.setLevel(logging.INFO)


class IgStatisticsService(cxmate.Service):

    def process(self, params, input_stream):
        logging.info(params)

        ig_networks = IgraphAdapter.to_igraph(input_stream)
        for net in ig_networks:

            net['label'] = 'out_net'

        return IgraphAdapter.from_igraph(ig_networks)


if __name__ == "__main__":

    analyzer = IgStatisticsService()
    logging.warn('Starting igraph analysis service...')
    analyzer.run()
