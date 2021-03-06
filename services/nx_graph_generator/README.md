# NetworkX Random Graph Generator Service

## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.


## Parameters
### Algorithm (string, default: `fast_gnp_random_graph`)
You can select a graph generator by adding query-string `algorithm`

e.g. 
` curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST "localhost?algorithm=gnm_random_graph" | jq
`

Random graph generator you can select are below.
- `fast_gnp_random_graph`
- `gnp_random_graph`
- `dense_gnm_random_graph`
- `gnm_random_graph`
- `erdos_renyi_graph`
- `binomial_graph`
- `newman_watts_strogatz_graph`
- `watts_strogatz_graph`
- `connected_watts_strogatz_graph`
- `random_regular_graph`
- `barabasi_albert_graph`
- `powerlaw_cluster_graph`
- `random_lobster`
- `random_powerlaw_tree`


### Generator's Parameters
You can also pass graph generator's parameters by adding query-string.
You can see parameters you can pass in the following link
https://networkx.github.io/documentation/development/reference/generators.html#module-networkx.generators.random_graphs

If you don't pass parameters, default parameters are passed.

## Input
Required CX input fields are:
- `networkAttributes`

## Output
- `nodes`
- `edges`
- `nodeAttributes`
- `edgeAttributes`
- `networkAttributes`


## Examples
__lobster_layout__
![lobster-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/nx_graph_generator/nx_graph_generator_lobster.png)

__watts_strogatz_layout__
![watts_strogatz-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/nx_graph_generator/nx_graph_generator_watts_strogatz.png)