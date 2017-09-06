import cxmate
import logging

import numpy as np
from graph_tool import all as gt

logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)

from Adapter import Adapter


class GtDrawHierarchyService(cxmate.Service):
    def __init__(self):
        self.parameter = ["layout"]

    def propagate_label(self, tgraph, sgraph):
        if 'label' not in tgraph.vp:
            tgraph.vp.label = tgraph.new_vp("string")
        attrs = {}
        for node in sgraph.vertices():
            node_id = get_node_id(sgraph, node)
            attrs[node_id] = sgraph.vp.label[node_id]
        for node in tgraph.vertices():
            node_id = get_node_id(tgraph, node)
            if node_id in attrs:
                tgraph.vp.label[node_id] = attrs[node_id]

    def copy_clabels(self, t, state):
        n = len(state.levels)
        bs = state.get_bs()
        node_num = len(bs[0])
        upper_level = range(node_num)
        for i in range(n):
            cl = t.new_vp("int")
            for node_id in range(node_num):
                cl[node_id] = bs[i][upper_level[node_id]]
            upper_level = cl
            label_name = "clabel" + str(i)
            t.vp[label_name] = cl
 
    def process(self, params, input_stream):
        logger.warn(params)

        parameter = {p: params[p] for p in self.parameter}
        g = Adapter.to_graph_tool(input_stream)
        state = gt.minimize_nested_blockmodel_dl(g[0], deg_corr=True)
        pos, t, tpos = gt.draw_hierarchy(state, output="output.pdf", **parameter)
        self.propagate_label(t, g[0])
        self.copy_clabels(t, state)
        # return Adapter.from_graph_tool(g, pos, params["only-layout"])
        return Adapter.from_graph_tool([t], tpos, params["only-layout"])
    

def get_node_id(g, node):
    return g.vp.id[int(node)] if "id" in g.vp else int(node)





if __name__ == "__main__":
    analyzer = GtDrawHierarchyService()
    logger.info('Starting graph-tool analysis service...')
    analyzer.run()
