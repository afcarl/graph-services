import cxmate


class NetworkElementBuilder(cxmate.service.NetworkElementBuilder):
    def Position(self, position, node_id):
        ele = self.new_element()
        coord = ele.CartesianCoordinate
        coord.nodeId = node_id
        coord.x = position[0]*2000
        coord.y = position[1]*2000
        return ele
