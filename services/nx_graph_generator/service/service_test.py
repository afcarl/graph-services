import unittest
import random

from RandomGraphGeneratorService import RandomGraphGeneratorService

class TestRandomGraphGeneratorService(unittest.TestCase):
    def test_fast_gnp_random_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "fast_gnp_random_graph"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_gnp_random_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "gnp_random_graph"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_dense_gnm_random_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "dense_gnm_random_graph"
        params["n"] = 100
        params["m"] = 300
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)
            self.assertEqual(g.number_of_edges(), 300)

    def test_gnm_random_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "gnm_random_graph"
        params["n"] = 100
        params["m"] = 300
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)
            self.assertEqual(g.number_of_edges(), 300)

    def test_erdos_renyi_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "erdos_renyi_graph"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_binomial_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "binomial_graph"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_newman_watts_strogatz_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "newman_watts_strogatz_graph"
        params["n"] = 100
        params["k"] = 4
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)
            for i in range(g.number_of_nodes()):
                assert g.degree(i) >= 4, "The degree less than specified number. algorithm:{a}, degree:{d}".format(a=params["algorithm"], d=g.degree(i))

    def test_watts_strogatz_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "watts_strogatz_graph"
        params["n"] = 100
        params["k"] = 4
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_connected_watts_strogatz_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "connected_watts_strogatz_graph"
        params["n"] = 100
        params["k"] = 4
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_random_regular_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "random_regular_graph"
        params["n"] = 100
        params["d"] = 3
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)
            for i in range(g.number_of_nodes()):
                self.assertEqual(g.degree(i), 3)

    def test_barabasi_albert_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "barabasi_albert_graph"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_powerlaw_cluster_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "powerlaw_cluster_graph"
        params["n"] = 20
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 20)

    def test_random_lobster(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "random_lobster"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            assert g, "random robster does not work"

    def test_random_powerlaw_tree(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params['algorithm'] = "random_powerlaw_tree"
        params["n"] = 100
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 100)

    def test_large_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params["n"] = 2000
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 2000)

    def test_empty_graph(self):
        RGGS = RandomGraphGeneratorService()
        params = {'algorithm': 'fast_gnp_random_graph', 'n': 10, 'm': 5, 'p': 0.3, 'k': 3, 'd': 3, 'seed': -1, 'directed': False, 'p1': 0.2, 'p2': 0.2, 'tries': 100, 'gamma': 3.0}
        params["n"] = 0
        gs = RGGS.generate_graph(params)
        for g in gs:
            self.assertEqual(g.number_of_nodes(), 0)


if __name__ == '__main__':
    unittest.main()