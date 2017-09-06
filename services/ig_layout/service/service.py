import cxmate
import logging
import igraph as ig
from Adapter import NetworkElementBuilder, IgraphAdapter

logger = logging.getLogger('igraph_service')
logger.setLevel(logging.INFO)


class IgCommunityService(cxmate.Service):

    def process(self, params, input_stream):
        for k, v in params.items():
            if v == 'None':
                del params[k]
            elif k in ['area']:
                params[k] = float(params[k])
            elif k in ['maxiter', 'maxdelta', 'repulserad', 'dim']:
                params[k] = int(params[k])
        logging.warn(params)
        ig_networks = IgraphAdapter.to_igraph(input_stream)
        pos_dict = {}

        for net in ig_networks:
            net['label'] = 'out_net'
            pos = net.layout_fruchterman_reingold(**params)
            for i, vertex in enumerate(net.vs):
                pos_dict[vertex['nodeId']] = pos[i]

        return self.outputStream(ig_networks, pos_dict)

    def outputStream(self, networks, pos):
        for i in IgraphAdapter.from_igraph(networks):
            yield i
        for k, v in pos.items():
            builder = NetworkElementBuilder('out_net')
            ele = builder.new_element()
            layout = ele.CartesianCoordinate
            layout.nodeId = k
            layout.x = v[0]
            layout.y = v[1]
            if len(v) == 3:
                # dim = 3
                layout.z = v[2]
            yield ele

if __name__ == "__main__":

    analyzer = IgCommunityService()
    logging.warn('Starting igraph analysis service...')
    analyzer.run()
