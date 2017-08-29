import cxmate
import networkx

from GraphGeneratorService import GraphGeneratorService


class RandomGraphGeneratorService(GraphGeneratorService):
    def __init__(self):
        self.algorithms = {
            "fast_gnp_random_graph": {"function":networkx.fast_gnp_random_graph, "parameter": ["n", "p", "seed", "directed"]},
            "gnp_random_graph": {"function":networkx.gnp_random_graph, "parameter": ["n", "p", "seed", "directed"]},
            "dense_gnm_random_graph": {"function":networkx.dense_gnm_random_graph, "parameter": ["n", "m", "seed"]},
            "gnm_random_graph": {"function":networkx.gnm_random_graph, "parameter": ["n", "m", "seed", "directed"]},
            "erdos_renyi_graph": {"function":networkx.erdos_renyi_graph, "parameter": ["n", "p", "seed", "directed"]},
            "binomial_graph": {"function":networkx.binomial_graph, "parameter": ["n", "p", "seed", "directed"]},
            "newman_watts_strogatz_graph": {"function":networkx.newman_watts_strogatz_graph, "parameter": ["n", "k", "p", "seed"]},
            "watts_strogatz_graph": {"function":networkx.watts_strogatz_graph, "parameter": ["n", "k", "p", "seed"]},
            "connected_watts_strogatz_graph": {"function":networkx.connected_watts_strogatz_graph, "parameter": ["n", "k", "p", "tries", "seed"]},
            "random_regular_graph": {"function":networkx.random_regular_graph, "parameter": ["d", "n", "seed"]},
            "barabasi_albert_graph": {"function":networkx.barabasi_albert_graph, "parameter": ["n", "m", "seed"]},
            "powerlaw_cluster_graph": {"function":networkx.powerlaw_cluster_graph, "parameter": ["n", "m", "p", "seed"]},
            # "random_kernel_graph": {"function":networkx.random_kernel_graph, "parameter": []},
            "random_lobster": {"function":networkx.random_lobster, "parameter": ["n", "p1", "p2", "seed"]},
            # "random_shell_graph": {"function":networkx.random_shell_graph, "parameter": ["constructor", "seed"]},  # not supported
            "random_powerlaw_tree": {"function":networkx.random_powerlaw_tree, "parameter": ["n", "gamma", "seed", "tries"]},
            # "random_powerlaw_tree_sequence": {"function":networkx.random_powerlaw_tree_sequence, "parameter": ["n", "gamma"]}, # not supported
        }

    def generate_graph(self, params):
        algorithm_name = params["algorithm"]
        algorithm = self.algorithms[algorithm_name]

        parameter = {p: params[p] for p in algorithm["parameter"]}
        if parameter["seed"] == -1:
            del parameter["seed"]
        network = algorithm["function"](**parameter)

        # this network doesn't have enough attributes to use cxmate.Adapter.from_networkx
        network.graph["label"] = "My output network"
        for n in network.nodes():
            network.node[n]["id"] = n
        for i, e in enumerate(network.edges()):
            s, t = e[0], e[1]
            network[s][t]["id"] = i
        yield network


if __name__ == "__main__":
  myService = RandomGraphGeneratorService()
  myService.run() #run starts the service listening for requests from cxMate

