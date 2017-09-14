const cxmate = require('cxmate');
const d3Hierarchy = require('d3-hierarchy');
const d3adapter = require('./d3Adapter');


class D3LayoutService extends cxmate.Service {

  process(params, elementStream) {

    // Extract required parameters from

    // ID of the tree root node
    const rootNodeId = params['root']

    // Layout type (circular or regular tree)
    const layoutType = params['type']


    d3adapter.toD3Tree(elementStream, rootNodeId, hierarchy => {

      applyClusterLayout(hierarchy)

      // TODO: implement this function and stream result
      d3adapter.fromD3Tree(hierarchy)
    });
  }

}

const applyClusterLayout = (hierarchy, areaSize=1600) => {
  const layout = d3Hierarchy
    .cluster()
    .size([360, areaSize])
    .separation((a, b) => (a.parent === b.parent ? 1:2)/a.depth)

  layout(hierarchy);

}

const project = (x, y) => {
  const angle = (x - 90) / 180 * Math.PI
  const radius = y
  return [
    radius * Math.cos(angle),
    radius * Math.sin(angle),
    angle
  ];
}



const layoutService = new D3LayoutService();
layoutService.run();
