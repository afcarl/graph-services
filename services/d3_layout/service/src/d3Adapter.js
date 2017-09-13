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

      networks[label].push({
        name: edge.sourceId,
        parent: edge.targetId,
      })
    }
  })

  is.on('end', () => {

    console.log('---END of stream ----')

    for (let network in networks) {
      console.log('--- Calling strat3  ----')

      console.log(networks[network])

      const net = d3Hierarchy.stratify()
        .id(d => d.name)
        .parentId(d => d.parent)(networks[network])

      callback(net)
    }
  })
}

const fromD3Tree = tree => {
  console.log('--- d3 tree 2 CX ----')
}


module.exports.toD3Tree = toD3Tree
module.exports.fromD3Tree = fromD3Tree
