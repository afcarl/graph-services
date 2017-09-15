# graph-tool Layout Service
## Introduction
graph-tool is a high-performance graph library using Boost Graph.  This is an example service to perform layout using graph-tool.


## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST "localhost:3000" | jq .```
1. Now you should get a network with some new network attributes.




# REST API Specification

## Path Parameters
### layout-name (string, default: `sfdp_layout`)
You can select a layout by adding query-string `layout-name`.

e.g. 
` curl --data "@sample.cx" -H "Content-type: application/json" "localhost?layout-name=sfdp_layout" | jq ".data" 
`

Layout names you can select are below.
- `sfdp_layout`
- `fruchterman_reingold_layout`
- `arf_layout`
- `radial_tree_layout`
- `planar_layout`
- `random_layout`

### root (int, default: `0`)
If you select `radial_tree_layout`, you can select root node by `root` parameter.

## Input
Required CX input fields are:

- `nodes`
- `edges`
- `nodeAttributes`
- `edgeAttributes`
- `networkAttributes`

## Output
- `cartesianLayout`

## Examples
__sfdp_layout__
![sfdp-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/gt_layout/gt_layout_sfdp.png)

__radial_tree_layout__
![radial_tree-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/gt_layout/gt_layout_radial_tree.png)

## Service Unit Test
From this directory, type below commands.
1. `docker build -t gt_layout_test -f ./service/ServiceTestDockerfile ./service`
2. `docker run gt_layout_test`

## Adapter Unit Test
From this directory, type below commands.
1. `docker build -t gt_adapter_test -f ./service/AdapterTestDockerfile ./service`
2. `docker run gt_adapter_test`
