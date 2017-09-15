const d3Hierarchy = require('d3-hierarchy')


const toD3Tree = (is, rootNodeId, callback) => {
  console.log('---From cx to d3 tree ----')

  const networks = {}

  is.on('data', networkElement => {

    const label = networkElement.label

    if (!(label in networks)) {
      networks[label] = [{name: rootNodeId, parent: ''}]
    }

    if (networkElement.element === 'edge') {

      const edge = networkElement.edge
      if (edge.sourceId === rootNodeId){
        console.log("The root node has parent. You must specify other node as 'root' parameter")
      }
      networks[label].push({
        name: edge.sourceId,
        parent: edge.targetId,
      })
    }
  })

  is.on('end', () => {
    console.log('---END of stream ----')
    for (let network in networks) {
      console.log(networks[network]);
      if (networks[network][0].name === 'root'){
        networks[network][0].name = findRoot(networks[network]);
      }
      console.log('--- Calling strat3  ----')

      // console.log(networks[network])
      // console.log(networks[network][0].name);

      const net = d3Hierarchy.stratify()
        .id(d => d.name)
        .parentId(d => d.parent)(networks[network])

      callback(net)
    }
  })
}


const findRoot = (network) => {
  parentNodeOf = {};
  for(let edge of network){
    parentNodeOf[edge.name] = edge.parent;
  }
  rootNode = network[1].name;
  visited = {};
  while(parentNodeOf[rootNode]){
    if (visited[rootNode]){
      console.log("There are loop in the network");
      return 0;
    }
    visited[rootNode] = true;
    rootNode = parentNodeOf[rootNode];
  }
  return rootNode;
}
/*const findRoot = (network) => {
  sources = [];
  targets = {};
  for(let edge of network){
    sources.push(edge.name);
    targets[edge.parent] = true;
  }
  root_canditates = sources.filter(node => !targets[node]);
  if (root_canditates.length < 0){
    console.log("There are no root candidate node.");
    return 0;
  }
  return root_canditates[0];
}*/


const fromD3Tree = (tree, label, callback) => {
  // TODO: data.represents
  // TODO: attribute
  // TODO: edge.interaction
  console.log('--- d3 tree 2 CX ----');
  // console.log(tree);

  // breadth first 
  let node_queue = [tree];
  for (let i = 0; i < node_queue.length; i++) {  // length will change during iteration.
    let node = node_queue[i];
    let node_id = node.id;
    let data = node.data;
    callback({
      label: label,
      element: 'node',
      node: {
        id: node_id,
        name: data.name,
        represents: "",
      },
    });
    callback({
      label: label,
      element: 'edge',
      edge: {
        id: i.toString(),
        sourceId: node_id,
        targetId: node.data.parent,
        interaction: "",
      },
    });
    callback({
      label: label,
      element: 'cartesianLayout',
      CartesianCoordinate: {
        "nodeId": node_id,
        "x": node.x,
        "y": node.y,
        "z": 0,
        "viewId":0
      },
    });
    Array.prototype.push.apply(node_queue, node.children);
    // for (let nodeAttr in data) {
    //   let type = typeof data[nodeAttr];
    //   callback({
    //     label: label,
    //     element: 'nodeAttribute',
    //     nodeAttribute: {
    //       nodeId: id,
    //       name: nodeAttr,
    //       value: data[nodeAttr].toString(),
    //       type: type,
    //     },
    //   });
    // }
  }
 
}


module.exports.toD3Tree = toD3Tree
module.exports.fromD3Tree = fromD3Tree
