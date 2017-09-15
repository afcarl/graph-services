# d3 layout Service
## Introduction

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
### type (string, default: `tree`)
You can select a layout by adding query-string `type`.

e.g. 
` curl --data "@sample.cx" -H "Content-type: application/json" "localhost?type=tree" | jq ".data" 
`

Layout names you can select are below.
- `tree`
- `circular`

### root (int, default: Find root node automatically if exists)
Unique ID of the root node of input tree.

## Input
Required CX input fields are:

- `edges`

## Output
- `cartesianLayout`

## Examples
__cicular__
![circular-example](https://raw.githubusercontent.com/idekerlab/graph-services/4e4ee735388bba4fd71fa5c9e6c7cf13c3d2daf8/services/d3_layout/d3_layout_circular.png)
