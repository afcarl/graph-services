import logging
from graph_tool import all as gt

logging.basicConfig(level=logging.DEBUG)

# Tag for default algorithm
DEFAULT_HANDLER = 'default'

class GtLayoutHandlers():
    """
    Provides actual layout algorithms from pre-defined
    list of graph-tool functions.
    """

    def __init__(self):
        self.__handlers = {
            'default': self.__sfdp_layout,

            "sfdp_layout": self.__sfdp_layout,
            "fruchterman_reingold_layout": self.__fruchterman_reingold_layout,
            "arf_layout": self.__arf_layout,
            "radial_tree_layout": self.__radial_tree_layout,
            "planar_layout": self.__planar_layout,
            "random_layout": self.__random_layout
            # "get_hierarchy_control_points": {"function": gt.get_hierarchy_control_points, "parameter": []},  # not supported
        }

    def get_handler(self, algorithm_name):
        if algorithm_name in self.__handlers:
            return self.__handlers[algorithm_name]
        else:
            logging.warn('Algorithm not available.  Using default one instead...')
            return self.__handlers[DEFAULT_HANDLER]

    def __sfdp_layout(self, net, **params):
        """
        :Graph net: A Graph
        :string vweight: Attribute name of vertex weight 
        :string eweight: Attribute name of edge weight
        :string pin: A name of vertex attribute with boolean values, which, if given, specify the vertices which will not have their positions modified.
        :string groups: A name of vertex attribute with group assignments. Vertices belonging to the same group will be put close together.
        :string pos: A name of initial vertex layout attribute. If not provided, it will be randomly chosen.
        """
        valid_params = {}
        vparam = ["vweight", "pin", "groups", "pos"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = ["eweight"]
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.sfdp_layout(net, **valid_params)

    def __fruchterman_reingold_layout(self, net, **params):
        """
        :Graph net: A Graph
        :string weight: Attribute name of an edge attribute with the respective weights
        :string pos: Attribute name of vector vertex property maps where the coordinates should be stored. If provided, this will also be used as the initial position of the vertices.
        """
        valid_params = {}
        vparam = ["pos"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = ["weight"]
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.fruchterman_reingold_layout(net, **valid_params)

    def __arf_layout(self, net, **params):
        """
        :Graph net: A Graph
        :string weight: Attribute name of an edge attribute with the respective weights
        :string pos: Attribute name of vector vertex property maps where the coordinates should be stored. If provided, this will also be used as the initial position of the vertices.
        """
        valid_params = {}
        vparam = ["pos"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = ["weight"]
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.arf_layout(net, **valid_params)

    def __radial_tree_layout(self, net, **params):
        """
        :Graph net: A Graph
        :int root: The root of the radial tree.
        :string rel_order : Attribute name of relative order of the nodes at each respective branch.
        :string node_weight : Attribute name of the relative spacing between leafs will correspond to the node weights.
        """
        valid_params = {"root": params["root"]}
        vparam = ["rel_order", "node_weight"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = []
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.radial_tree_layout(net, **valid_params)

    def __planar_layout(self, net, **params):
        """
        :Graph net: A Graph
        :string pos: Attribute name of vector vertex property maps where the coordinates should be stored. If provided, this will also be used as the initial position of the vertices.
        """
        valid_params = {}
        vparam = ["pos"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = []
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.planar_layout(net, **valid_params)

    def __random_layout(self, net, **params):
        """
        :Graph net: A Graph
        :string pos: Attribute name of vector vertex property maps where the coordinates should be stored. If provided, this will also be used as the initial position of the vertices.
        """
        valid_params = {}
        vparam = ["pos"]
        for param_name in vparam:
            if params[param_name] in net.vp:
                 valid_params[param_name] = net.vp[params[param_name]]
        eparam = []
        for param_name in eparam:
            if params[param_name] in net.ep:
                 valid_params[param_name] = net.ep[params[param_name]]
        return gt.random_layout(net, **valid_params)

