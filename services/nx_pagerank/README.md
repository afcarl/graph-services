# NetworkX Pagerank Services
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

### _is_directed_
Whether input network is directed graph or not

#### Default value
**True**

### _alpha_
Damping parameter for PageRank

#### Default value
**0.85**

### _personalization_
The “personalization vector” consisting of a dictionary with a key for every graph node and nonzero personalization value for each node. By default, a uniform distribution is used

#### Default value
**None**

### _max_iter_
Maximum number of iterations in power method eigenvalue solver

#### Default value
**100**

### _tol_
Error tolerance used to check convergence in power method solver

#### Default value
**0.000001**

### _nstart_
Starting value of PageRank iteration for each node

#### Default value
**None**

### _weight_
Edge data key to use as weight. If None weights are set to 1

#### Default value
**weight**

### _dangling_
The outedges to be assigned to any “dangling” nodes, i.e., nodes without any outedges. The dict key is the node the outedge points to and the dict value is the weight of that outedge. By default, dangling nodes are given outedges according to the personalization vector (uniform if not specified). This must be selected to result in an irreducible transition matrix (see notes under google_matrix). It may be common to have the dangling dict to be the same as the personalization dict

#### Default value
**None**


Example:

```http://localhost:8080?is_directed=False```

## Body
Required CX input fields are:

* nodes
* edges

## Output

* nodeAttributes
