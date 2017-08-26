import networkx as nx
import cxmate


class HelloService(cxmate.Service):

    def process(self, params, input_stream):
        network = cxmate.Adapter.to_networkx(input_stream)

        # Dummy service here...
        print('OK')
        return cxmate.Adapter.from_networkx(network)


if __name__ == "__main__":
  my_service = HelloService()
  my_service.run()
