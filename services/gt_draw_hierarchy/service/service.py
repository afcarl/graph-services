import cxmate
import logging

from graph_tool import all as gt
from Adapter import GraphToolAdapter

logging.basicConfig(level=logging.DEBUG)

# Label for CXmate output
OUTPUT_LABEL = 'out_net'

class GtDrawHierarchyService(cxmate.Service):
    """
    CI service for getting a hierarchically clustered network with layout
    """
    def __init__(self):
        super(cxmate.Service, self).__init__()
        self.parameter = ["layout", "beta", "deg_order", "deg_size", "vsize_scale", "hsize_scale", "hshortcuts", "hide", "bip_aspect", "empty_branches"]

    def process(self, params, input_stream):
        logging.debug(params)

        # Convert to graph-tool objects
        gs = GraphToolAdapter.to_graph_tool(input_stream)
        ts, tposs = self.process_graphs(params, gs)
        return GraphToolAdapter.from_graph_tool(ts, tposs, False)

    def process_graphs(self, params, gs):
        """
        :params params: Dict of parameter.
        :params gs: A list of graph-tool's Graph objects
        :returns: A Graph object and its layout
        """
        parameter = {p: params[p] for p in self.parameter}

        ts = []
        tposs = []
        for g in gs:
            if g.num_vertices() <= 1:
                ts.append(g)
                tpos = gt.sfdp_layout(g)
                tposs.append(tpos)
                continue
            state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
            pos, t, tpos = gt.draw_hierarchy(state, output="output.pdf", **parameter)
            self.add_edge_id(t)
            self.propagate_label(t, g)
            self.copy_clabels(t, state)
            t.gp.label = t.new_gp("string")
            t.gp.label = OUTPUT_LABEL
            ts.append(t)
            tposs.append(tpos)
        return ts, tposs

    def propagate_label(self, tgraph, sgraph):
        """
        Make nodes in tgraph has same "label" attribute as nodes in sgraph
        """
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
        """
        Copy "clabel{n}" attributes from state to t
        :Graph t: a Graph
        :State state: 
        """
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
        """
        Add "id" attribute to the edges in Graph t
        """
        if "id" not in t.ep:
            t.ep.id = t.new_ep("int")
        for i, edge in enumerate(t.edges()):
            t.ep.id[edge] = i


def get_node_id(g, node):
    """
    get id attribute or index of node in g
    :Graph g: a Graph
    :Node node: 
    """
    return g.vp.id[int(node)] if "id" in g.vp else int(node)


if __name__ == "__main__":
    analyzer = GtDrawHierarchyService()
    logging.info('Starting graph-tool draw hierarchy service...')
    analyzer.run()
