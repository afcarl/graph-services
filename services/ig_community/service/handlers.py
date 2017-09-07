import logging
logging.basicConfig(level=logging.DEBUG)

# Tag for default algorithm
DEFAULT_HANDLER = 'default'

# Attribute name for the communities
COMMUNITY = 'community'



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

    def __label_propagation(self, net, **params):
        # TODO: extract other parameters
        cluster = net.community_label_propagation(**params)
        net.vs[COMMUNITY] = cluster.membership
        self.__assign_edge_membership(net, cluster)

    def __fastgreedy(self, net, **params):
        # TODO: extract other parameters
        cluster = net.community_fastgreedy().as_clustering()
        net.vs[COMMUNITY] = cluster.membership
        self.__assign_edge_membership(net, cluster)


    def __optimal_modularity(self, net, **params):

        # TODO: this does not work.  weights should be List
        cluster = net.community_optimal_modularity(weights=params['weights'])
        net.vs[COMMUNITY] = cluster.membership
        net['modularity'] = cluster.modularity
        self.__assign_edge_membership(net, cluster)

    def __leading_eigenvector(self, net, **params):

        # TODO: extract other parameters
        cluster = net.community_leading_eigenvector(clusters=self.__get_community_count(**params))
        net.vs[COMMUNITY] = cluster.membership
        self.__assign_edge_membership(net, cluster)

    def __edge_betweenness(self, net, **params):
        # TODO: extract other parameters

        cluster = net.community_edge_betweenness(clusters=self.__get_community_count(**params))\
            .as_clustering()
        net.vs[COMMUNITY] = cluster.membership
        self.__assign_edge_membership(net, cluster)

    def __get_community_count(self, **params):
        cluster_count = params['clusters']
        if cluster_count == -1:
            cluster_count = None

        return cluster_count

    def __assign_edge_membership(self, net, cluster):
        for edge in net.es:
            if cluster.membership[edge.source] == cluster.membership[edge.target]:
                edge[COMMUNITY] = cluster.membership[edge.source]
