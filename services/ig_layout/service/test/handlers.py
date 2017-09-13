import logging
logging.basicConfig(level=logging.DEBUG)

# Tag for default algorithm
DEFAULT_HANDLER = 'default'


class IgLayoutHandlers():
    """
    Provides actual community detection algorithms from pre-defined
    list of igraph functions.

    """

    def __init__(self):

        self.__handlers = {
            'default': self.__circle,

            'bipartite': self.__bipartite,
            'circle': self.__circle,
            'drl': self.__drl,
            'fruchterman_reingold': self.__fruchterman_reingold,
            'graphopt': self.__graphopt,
            'grid': self.__grid,
            'kamada_kawai': self.__kamada_kawai,
            'lgl': self.__lgl,
            'random': self.__random,
            'reingold_tilford': self.__reingold_tilford,
            'reingold_tilford_circular': self.__reingold_tilford_circular,
            'star': self.__star
        }

    def get_handler(self, algorithm_name):

        if algorithm_name in self.__handlers:
            logging.debug("algorithm_name: {}".format(algorithm_name))
            return self.__handlers[algorithm_name]
        else:
            logging.warn('Algorithm not available.  Using default one instead...')
            return self.__handlers[DEFAULT_HANDLER]

    def __bipartite(self, net, **params):
        parameters_list = ['types', 'hgap', 'vgap', 'maxiter']
        params = {i: params[i] for i in parameters_list}
        params['types'] = net.vs[params['types']] if params['types'] is not None else None
        params['maxiter'] = net.vs[params['maxiter']] if params['maxiter'] is not None else 100
        logging.debug(params)
        pos = net.layout_bipartite(**params)
        return pos

    def __circle(self, net, **params):
        parameters_list = ['dim']
        params = {i: params[i] for i in parameters_list}
        logging.debug(params)
        pos = net.layout_circle(**params)
        return pos

    def __drl(self, net, **params):
        parameters_list = ['weights', 'fixed', 'seed', 'options', 'dim']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None
        params['fixed'] = net.vs[params['fixed']] if params['fixed'] is not None else None
        # parameter 'seed' is not supported now.
        params['seed'] = None
        logging.debug(params)
        pos = net.layout_drl(**params)
        return pos

    def __fruchterman_reingold(self, net, **params):
        parameters_list = ['weights', 'maxiter', 'maxdelta', 'area', 'coolexp', 'repulserad', 'minx', 'maxx', 'miny', 'maxy', 'minz', 'maxz', 'seed', 'dim']
        params = {i: params[i] for i in parameters_list}
        params['weights'] = net.es[params['weights']] if params['weights'] is not None else None
        params['maxiter'] = net.vs[params['maxiter']] if params['maxiter'] is not None else 500
        params['coolexp'] = net.vs[params['coolexp']] if params['coolexp'] is not None else 1.5
        vs_params = ['minx', 'maxx', 'miny', 'maxy', 'minz', 'maxz']
        for p in vs_params:
            params[p] = net.vs[params[p]] if params[p] is not None else None
        # parameter 'seed' is not supported now.
        params['seed'] = None
        logging.debug(params)
        pos = net.layout_fruchterman_reingold(**params)
        return pos

    def __graphopt(self, net, **params):
        parameters_list = ['niter', 'node_charge', 'node_mass', 'spring_length', 'spring_constant', 'max_sa_movement', 'seed']
        params = {i: params[i] for i in parameters_list}
        # parameter 'seed' is not supported now.
        params['seed'] = None
        logging.debug(params)
        pos = net.layout_graphopt(**params)
        return pos

    def __grid(self, net, **params):
        parameters_list = ['width', 'height', 'dim']
        params = {i: params[i] for i in parameters_list}
        logging.debug(params)
        pos = net.layout_grid(**params)
        return pos

    def __kamada_kawai(self, net, **params):
        parameters_list = ['maxiter', 'sigma', 'initemp', 'coolexp', 'kkconst', 'minx', 'maxx', 'miny', 'maxy', 'minz', 'maxz', 'seed', 'dim']
        params = {i: params[i] for i in parameters_list}
        params['maxiter'] = net.vs[params['maxiter']] if params['maxiter'] is not None else 1000
        params['coolexp'] = net.vs[params['coolexp']] if params['coolexp'] is not None else 0.99
        vs_params = ['minx', 'maxx', 'miny', 'maxy', 'minz', 'maxz']
        for p in vs_params:
            params[p] = net.es[params[p]] if params[p] is not None else None
        # parameter 'seed' is not supported now.
        params['seed'] = None
        logging.debug(params)
        pos = net.layout_kamada_kawai(**params)
        return pos

    def __lgl(self, net, **params):
        parameters_list = ['maxiter', 'maxdelta', 'area', 'coolexp', 'repulserad', 'cellsize', 'root']
        params = {i: params[i] for i in parameters_list}
        params['maxiter'] = net.vs[params['maxiter']] if params['maxiter'] is not None else 150
        params['coolexp'] = net.vs[params['coolexp']] if params['coolexp'] is not None else 1.5
        # parameter 'root' is not supported now.
        params['root'] = None
        logging.debug(params)
        pos = net.layout_lgl(**params)
        return pos

    def __random(self, net, **params):
        parameters_list = ['dim']
        params = {i: params[i] for i in parameters_list}
        logging.debug(params)
        pos = net.layout_random(**params)
        return pos

    def __reingold_tilford(self, net, **params):
        # TODO: Fix a bug
        parameters_list = ['mode', 'root', 'rootlevel']
        params = {i: params[i] for i in parameters_list}
        # parameter 'root' and 'rootlevel' are not supported now.
        params['root'] = None
        params['rootlevel'] = None
        logging.debug(params)
        pos = net.layout_reingold_tilford(**params)
        return pos

    def __reingold_tilford_circular(self, net, **params):
        # TODO: Fix a bug
        parameters_list = ['mode', 'root', 'rootlevel']
        params = {i: params[i] for i in parameters_list}
        # parameter 'root' and 'rootlevel' are not supported now.
        params['root'] = None
        params['rootlevel'] = None
        logging.debug(params)
        pos = net.layout_reingold_tilford_circular(**params)
        return pos

    def __star(self, net, **params):
        parameters_list = ['center', 'order']
        params = {i: params[i] for i in parameters_list}
        params['order'] = net.es[params['order']] if params['order'] is not None else None
        # parameter 'center' is not supported now.
        params['center'] = None
        logging.debug(params)
        pos = net.layout_star(**params)
        return pos

