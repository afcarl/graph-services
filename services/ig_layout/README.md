# igraph Layout Service Example
igraph layout_fruchterman_reingold service

## Quick Start

1. Install Docker: https://store.docker.com/search?type=edition&offering=community
1. (Optional) Install jq
1. Make sure you also have latest version of Docker Compose
1. From this directory, type ```docker-compose build && docker-compose up```
1. ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.


(TBD)

# REST API Specification

## Path Parameters

<!--
### _weights_
edge weights to be used. Can be a sequence or iterable or even an edge attribute name.
-->

#### Default value
**None**


### _maxiter_
the number of iterations to perform.

#### Default value
**500**


### _maxdelta_
the maximum distance to move a vertex in an iteration.

#### Default value
**None (the number of vertices)**


### _area_
the area of the square on which the vertices will be placed. 
#### Default value
**None (the square of the number of vertices)**


### _coolexp_
The cooling exponent of the simulated annealing.

#### Default value
**1.5**


### _repulserad_
determines the radius at which vertex-vertex repulsion cancels out attraction of adjacent vertices.

#### Default value
**None (the number of vertices^3)**


### _seed_
if None, uses a random starting layout for the algorithm. If a matrix (list of lists), uses the given matrix as the starting position.

#### Default value
**None**


### _dim_
the desired number of dimensions for the layout. dim=2 means a 2D layout, dim=3 means a 3D layout.

#### Default value
**2**


Example:

```http://localhost:8080?maxiter=1000```

## Body
Required CX input fields are:

* nodes
* edges

## Output

* cartesianLayout
