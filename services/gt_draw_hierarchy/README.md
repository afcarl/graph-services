# graph-tool Service Example
## Introduction
graph-tool is a high-performance graph library using Boost Graph.  This is an example service to perform layout using graph-tool.


## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.




# REST API Specification

## Path Parameters
### layout
You can select a layout by adding query-string `layout`.
The default value is `radial`

e.g. 
` curl --data "@sample.cx" -H "Content-type: application/json" "localhost?layout=radial" | jq ".data" 
`

Layout names you can select are below.
- `sfdp`
- `radial`

### only-layout
`only-layout` indicates whether the output is only layout or with network itself.
The default value is `True`.


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

