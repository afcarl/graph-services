# graph-tool draw_hierarchy Service
## Introduction
graph-tool is a high-performance graph library using Boost Graph.  This is an example service to perform layout using graph-tool.


## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.
TODO: more parameter



# REST API Specification

## Path Parameters
### layout (string, default: `radial`)
You can select a layout by adding query-string `layout`.

e.g. 
` curl --data "@sample.cx" -H "Content-type: application/json" "localhost?layout=radial" | jq ".data" 
`

Layout names you can select are below.
- `sfdp`
- `radial`

### beta (int, default: `8`)
Edge bundling strength.

### deg_order (boolean, default: `True`)
If True, the vertices will be ordered according to degree inside each group.

### deg_size (boolean, default: `True`)
If True, the (total) node degrees will be used for the default vertex sizes.

### vsize_scale (number, default: `1`)
Multiplicative factor for the default vertex sizes.

### hsize_scale (number, default: `1`)
Multiplicative factor for the default sizes of the hierarchy nodes.

### hshortcuts (int, default: `0`)
Include shortcuts to the number of upper layers in the hierarchy determined by this parameter.

### hide (int, default: `0`)
Hide upper levels of the hierarchy.

### bip_aspect (number, default: `1`)
If layout == bipartite, this will define the aspect ratio of layout.

### empty_branches (boolean, default: `False`)
If empty_branches == False, dangling branches at the upper layers will be pruned.

### only-layout (boolean, default: `True`)
`only-layout` indicates whether the output is only layout or with network itself.


## Input
Required CX input fields are:

- `nodes`
- `edges`
- `nodeAttributes`
- `edgeAttributes`
- `networkAttributes`

## Output
- `nodes`
- `edges`
- `nodeAttributes`
- `edgeAttributes`
- `networkAttributes`
- `cartesianLayout`

## Service Unit Test
From this directory, type below commands.
1. `docker build -t gt_draw_hierarchy_test -f ./service/ServiceTestDockerfile ./service`
2. `docker run gt_draw_hierarchy_test`

## Adapter Unit Test
From this directory, type below commands.
1. `docker build -t gt_adapter_test -f ./service/AdapterTestDockerfile ./service`
2. `docker run gt_adapter_test`

## Examples
__radial__
![radial-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/gt_draw_hierarchy/gt_draw_hierarchy_radial.png)
