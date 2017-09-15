const cxmate = require('cxmate');
const d3Hierarchy = require('d3-hierarchy');
const d3adapter = require('./d3Adapter');

// Label for CXmate output
const OUTPUT_LABEL = 'Output';
class D3LayoutService extends cxmate.Service {

  process(params, elementStream) {
    console.log(params);

    // Extract required parameters from

    // ID of the tree root node
    const rootNodeId = params['root']

    // Layout type (circular or regular tree)
    const layoutType = params['type']
    const circular = layoutType === 'circular';

    d3adapter.toD3Tree(elementStream, rootNodeId, hierarchy => {
      applyClusterLayout(hierarchy)
      if (circular){
        console.log("circular");
        hierarchy = extractPositions(hierarchy, circular);
      }
      d3adapter.fromD3Tree(hierarchy, OUTPUT_LABEL, (element) =>{
        elementStream.write(element);
      });
      elementStream.end();
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
const extractPositions = (d3Tree, circular) => {
  return walk(d3Tree, d3Tree, circular)
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

const walk = (node, root, circular) => {
  let newPos = [node.x, node.y]
  if(circular) {
    newPos = project(node.x, node.y)
  }
  node.x = newPos[0];
  node.y = newPos[1];

  const children = node.children

  if (children !== undefined && children.length !== 0) {
    children.forEach(child => walk(child, root, circular))
  }
  return root
}


const layoutService = new D3LayoutService();
layoutService.run();
