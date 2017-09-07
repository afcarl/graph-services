import cxmate
import logging

import numpy as np
from graph_tool import all as gt

logger = logging.getLogger('graph_tool_service')
logger.setLevel(logging.INFO)

from Adapter import Adapter


class GtDrawHierarchyService(cxmate.Service):
    def __init__(self):
        super(cxmate.Service, self).__init__()
        self.parameter = ["layout"]

    def propagate_label(self, tgraph, sgraph):
        if 'label' not in sgraph.vp:
            return
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
            label_name = "clabel" + str(i)
            cl = t.new_vp("int")
            cl.a.fill(-2)
            for node_id in range(node_num):  # for original nodes
                cl[node_id] = bs[i][upper_level[node_id]]
            upper_level = cl

            # for not original nodes.
            for edge in t.edges():
                target_label = cl[edge.target()]
                source_label = cl[edge.source()]
                if source_label == -2:  # first edge
                    cl[edge.source()] = target_label
                elif source_label in (-1, target_label):
                    pass  # already cl[edge.source()] = -1
                else:  # source node is connected with different clusters. i.e. it is a branch.
                    cl[edge.source()] = -1

            # for edges
            cle = t.new_ep("int")
            for edge in t.edges():
                source_label = cl[edge.source()]
                cle[edge] = source_label
            t.vp[label_name] = cl
            t.ep[label_name] = cle

    def add_edge_id(self, t):
        if "id" not in t.ep:
            t.ep.id = t.new_ep("int")
            t.ep.label = t.new_ep("int")
        for i, edge in enumerate(t.edges()):
            t.ep.id[edge] = i
            t.ep.label[edge] = i
 
    def process(self, params, input_stream):
        logger.warn(params)

        parameter = {p: params[p] for p in self.parameter}
        g = Adapter.to_graph_tool(input_stream)
        state = gt.minimize_nested_blockmodel_dl(g[0], deg_corr=True)
        pos, t, tpos = gt.draw_hierarchy(state, output="output.pdf", **parameter)
        self.add_edge_id(t)
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
