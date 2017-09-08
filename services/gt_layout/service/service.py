import cxmate
import logging

from handlers import GtLayoutHandlers
from Adapter import GraphToolAdapter
logging.basicConfig(level=logging.DEBUG)

# Label for CXmate output
OUTPUT_LABEL = 'out_net'

# Layout algorithm name
LAYOUT_NAME = 'layout-name'


class GtLayoutService(cxmate.Service):
    def __init__(self):
        self.__handlers = GtLayoutHandlers()

    def process(self, params, input_stream):
        logging.debug(params)

        layout_name = params.pop(LAYOUT_NAME)
        ol = params.pop("only-layout")

        # Get the layout function by name of the algorithm
        handler = self.__handlers.get_handler(layout_name)

        gs = GraphToolAdapter.to_graph_tool(input_stream)
        poss = []
        for g in gs:
            # Call the function to get position
            g.gp.label = g.new_gp("string")
            g.gp.label = OUTPUT_LABEL
            pos = handler(g, **params)
            poss.append(pos)
        return GraphToolAdapter.from_graph_tool(gs, poss, ol)


if __name__ == "__main__":
    analyzer = GtLayoutService()
    logging.info('Starting graph-tool layout service...')
    analyzer.run()
