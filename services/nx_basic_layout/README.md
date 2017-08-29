# Basic Layout Service Example

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

### _layout-name_
Name of the layout algorithm

#### Default value
**circular**

#### Available values
* circular
* spring


Example:

```http://localhost:8080?layout-name=spring```

## Body
Required CX input fields are:

* nodes
* edges

## Output

* cartesianLayout
