# igraph Community Service
## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.


(TBD)

## Path Parameters

### _type_
Type of community algorithm

* label_propagation
* optimal_modularity  
    _optimal_modularity_ is  **unlikely to work for graphs larger than a few (less than a hundred) vertices.**


### _weights_
Name of an edge attribute or a list containing edge weights.

#### Default value
**None**


### _initial  (label_propagation)_
Name of a vertex attribute or a list containing the initial vertex labels.

#### Default value
**None**


### _fixed  (label_propagation)_
A list of booleans for each vertex. True corresponds to vertices whose labeling should not change during the algorithm.

#### Default value
**None**


Example:

```http://localhost:8080?type=label_propagation```

## Body
Required input fields are:

* nodes
* edges

## Output

* nodeAttributes
