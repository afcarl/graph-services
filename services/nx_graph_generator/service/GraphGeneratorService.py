import cxmate
import networkx
import logging
logging.basicConfig(level=logging.DEBUG)


class GraphGeneratorService(cxmate.Service):
    def process(self, params, input_stream):
        """
        process is a required method, if it's not implemented, cxmate.service will throw an error
        this process implementation will echo the received network back to the sender

        :param input_stream: a python generator that returns CX elements
        :returns: a python generator that returns CX elements
        """
        logging.debug(params)
        for x in input_stream:
            pass
        network = self.generate_graph(params)
        cx = cxmate.Adapter.from_networkx(network)
        return cx

    def generate_graph(self, params):
        raise NotImplementedError


if __name__ == "__main__":
    logging.info('Starting networkx random graph generator service...')
    myService = GraphGeneratorService()
    myService.run() #run starts the service listening for requests from cxMate

