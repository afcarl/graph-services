# Introduction to CX Mate for Python users

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
Type of analysis to be performed

* betweenness
* degree
* closeness


Example:

```http://localhost:8080?type=degree```

## Body
Required input fields are:

* nodes
* edges

## Output

* nodeAttributes
