# NetworkX Layout Services
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

### _prog_
Name of Graphviz layout program

#### Default value
**neato**

### _root_
Root node for twopi layout

#### Default value
**None**


#### Available values
* neato
* dot
* fdp
* circo
* twopi


Example:

```http://localhost:8080?neato=dot```

## Body
Required CX input fields are:

* nodes
* edges

## Output

* cartesianLayout
