import cxmate


class NetworkElementBuilder(cxmate.service.NetworkElementBuilder):
    def Position(self, position, node_id):
        ele = self.new_element()
        coord = ele.CartesianCoordinate
        coord.nodeId = node_id
        coord.x = position[0] * 100
        coord.y = position[1] * 100
        return ele
