import cxmate
import logging
from Adapter import IgraphAdapter
from handlers import CommunityDetectionHandlers

logging.basicConfig(level=logging.DEBUG)

# Label for CXmate output
OUTPUT_LABEL = 'out_net'

# Community detection algorithm name
ALGORITHM_TYPE = 'type'

# Palette name
PALETTE_NAME = 'palette'


class IgCommunityDetectionService(cxmate.Service):
    """
    CI service for detecting communities in the given network data
    """

    def __init__(self):
        self.__handlers = CommunityDetectionHandlers()

    def process(self, params, input_stream):
        logging.debug(params)
        algorithm_type = params[ALGORITHM_TYPE]
        del params[ALGORITHM_TYPE]

        palette = params[PALETTE_NAME]
        del params[PALETTE_NAME]

        # Replace string None to Python None data type
        for k, v in params.items():
            if v == str(None):
                params[k] = None

        # Convert to igraph objects
        ig_networks = IgraphAdapter.to_igraph(input_stream)

        for net in ig_networks:
            net['label'] = OUTPUT_LABEL

            # Get the community detection function by name of the algorithm
            handler = self.__handlers.get_handler(algorithm_type)

            # Call the function to detect community
            handler(net, palette, **params)

        return IgraphAdapter.from_igraph(ig_networks)



if __name__ == "__main__":
    analyzer = IgCommunityDetectionService()
    logging.info('Starting igraph community detection service...')
    analyzer.run()
