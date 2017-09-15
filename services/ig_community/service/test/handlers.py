import logging
import seaborn as sns
logging.basicConfig(level=logging.DEBUG)

# Tag for default algorithm
DEFAULT_HANDLER = 'default'

# Attribute name for the communities
COMMUNITY = 'community'

# Palette name
PALETTE_NAME = 'palette'


class CommunityDetectionHandlers():
    """
    Provides actual community detection algorithms from pre-defined
    list of igraph functions.

    If
    """

    def __init__(self):

        self.__handlers = {
            'default': self.__fastgreedy,

            'fastgreedy': self.__fastgreedy,
            'label_propagation': self.__label_propagation,
            'optimal_modularity': self.__optimal_modularity,
            'leading_eigenvector': self.__leading_eigenvector,
            'edge_betweenness': self.__edge_betweenness
        }

    def get_handler(self, algorithm_name):

        if algorithm_name in self.__handlers:
            return self.__handlers[algorithm_name]
        else:
            logging.warn('Algorithm not available.  Using default one instead...')
            return self.__handlers[DEFAULT_HANDLER]

    def __label_propagation(self, net, palette, **params):
        parameters_list = ['weights', 'initial', 'fixed']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None
        params['initial'] = net.vs[params['initial']] if params['initial'] is not None else None
        params['fixed'] = net.vs[params['fixed']] if params['fixed'] is not None else None

        cluster = net.community_label_propagation(**params)
        self.__assign_node_membership(net, cluster, palette)
        self.__assign_edge_membership(net, cluster)

    def __fastgreedy(self, net, palette, **params):
        if True in net.is_multiple():
            logging.error('fastgreedy doesn\'t support for multiple edges...')
        parameters_list = ['weights']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None

        cluster = net.community_fastgreedy(**params).as_clustering()
        self.__assign_node_membership(net, cluster, palette)
        self.__assign_edge_membership(net, cluster)

    def __optimal_modularity(self, net, palette, **params):
        parameters_list = ['weights']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None

        cluster = net.community_optimal_modularity(**params)
        net['modularity'] = cluster.modularity
        self.__assign_node_membership(net, cluster, palette)
        self.__assign_edge_membership(net, cluster)

    def __leading_eigenvector(self, net, palette, **params):
        parameters_list = ['weights', 'clusters']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None
        params['clusters'] = self.__get_community_count(**params)

        cluster = net.community_leading_eigenvector(**params)
        self.__assign_node_membership(net, cluster, palette)
        self.__assign_edge_membership(net, cluster)

    def __edge_betweenness(self, net, palette, **params):
        parameters_list = ['weights', 'clusters']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None
        # By default, igraph Adapter generates undirected graph
        params['directed'] = False
        params['clusters'] = self.__get_community_count(**params)

        cluster = net.community_edge_betweenness(**params).as_clustering()
        self.__assign_node_membership(net, cluster, palette)
        self.__assign_edge_membership(net, cluster)

    def __get_community_count(self, **params):
        cluster_count = params['clusters']
        if cluster_count == -1:
            cluster_count = None
        return cluster_count

    def __assign_edge_membership(self, net, cluster):
        for edge in net.es:
            if cluster.membership[edge.source] == cluster.membership[edge.target]:
                edge[COMMUNITY+'.color'] = net.vs[edge.source][COMMUNITY+'.color']
        
    def __assign_node_membership(self, net, cluster, palette):
        net.vs[COMMUNITY] = cluster.membership
        sns.set_palette(palette=palette, n_colors=len(cluster.sizes()))
        color = sns.color_palette(n_colors=len(cluster.sizes())).as_hex()
        logging.warning(color)
        for node in net.vs:
            node[COMMUNITY+'.color'] = color[node[COMMUNITY]]