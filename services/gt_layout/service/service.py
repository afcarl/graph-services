import cxmate
import logging
import itertools

import numpy as np
from graph_tool import all as gt

logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)

from Adapter import Adapter


class GtLayoutService(cxmate.Service):
    def __init__(self):
        self.layouts = {
            "sfdp_layout": {"function": gt.sfdp_layout, "parameter": []},
            "fruchterman_reingold_layout": {"function": gt.fruchterman_reingold_layout, "parameter": []},
            "arf_layout": {"function": gt.arf_layout, "parameter": []},
            "radial_tree_layout": {"function": gt.radial_tree_layout, "parameter": ["root"]},
            "planar_layout": {"function": gt.planar_layout, "parameter": []},
            "random_layout": {"function": gt.random_layout, "parameter": []},
            # "get_hierarchy_control_points": {"function": gt.get_hierarchy_control_points, "parameter": []},  # not supported
        }

    def process(self, params, input_stream):
        logger.warn(params)
        layout_name = params["layout-name"]
        layout = self.layouts[layout_name]

        parameter = {p: params[p] for p in layout["parameter"]}

        g = Adapter.to_graph_tool(input_stream)
        pos = layout["function"](g[0], **parameter)
        return Adapter.from_graph_tool(g, pos, params["only-layout"])


if __name__ == "__main__":
    analyzer = GtLayoutService()
    logger.info('Starting graph-tool analysis service...')
    analyzer.run()
