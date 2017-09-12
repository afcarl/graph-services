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
Whether input network is directed graph or not.

#### Default value
**True**

### _alpha_
Damping parameter for PageRank.

#### Default value
**0.85**

### _max_iter_
Maximum number of iterations in power method eigenvalue solver.

#### Default value
**100**

### _tol_
Error tolerance used to check convergence in power method solver.

#### Default value
**0.000001**

### _personalization_
The “personalization vector” consisting of a dictionary with a key for every graph node and nonzero personalization value for each node. The nodeAttribute can be used. If _None_ (default), a uniform distribution is used.

#### Default value
**None**

### _nstart_
Starting value of PageRank iteration for each node. The nodeAttribute can be used.

#### Default value
**None**

### _weight_
Edge data key to use as weight. The edgeAttribute can be used. If None weights are set to 1.

#### Default value
**None**

### _dangling_
The outedges to be assigned to any “dangling” nodes, i.e., nodes without any outedges. The nodeAttribute can be used.

#### Default value
**None**


Example:

```http://localhost:8080?is_directed=False&dangling=dangling```

## Body
Required CX input fields are:

* nodes
* edges
* nodeAttributes
* edgeAttributes


## Output

* nodeAttributes
