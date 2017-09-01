# Cytoscape CI Services for Graph Layouts and Analysis

## Introduction

This is the repository for sample implementations of Cytoscape CI services using [cxmate](https://github.com/cxmate/cxmate).

## Quick Start

All services in this repository have Dockerfile and easiest way to try these is using Docker Compose.

### Prerequisite

You need to install the following applications to run the services:

- Latest version of Docker CE/EE
- Docker Compose
- (Optional) [jq](https://stedolan.github.io/jq/) - for viewing results

**OR**

- Python 2/3 environment

  - You need to install the dependencies manually if you choose this option (TBD)

### How to run the _Hello World_ service

1. Make sure you have the latest version of Docker Compose
1. cd to ```services/hello_world_
1. From this directory, type ```docker-compose build && docker-compose up```
1. For the first time, this process takes minutes because it downloads a lot of dependencies over the internet.
1. After the build process, it automatically starts two services:
    - **cxmate** - An utility converting your data into CX
    - **hello_world python service** - A simple service adding some network attributes to the input network
1. Try ```curl -d "@./sample-data/sample.cx" -H "Content-Type: application/json" -X POST localhost | jq .```
1. Now you should get a network with some new network attributes.


## Project Structure

### _Services_ directory
This is the directory for the actual services.  Each directory contains one python service and associated cxmate instance.

### _Notebooks_ directory
This is the directory for sample Jupyter notebooks calling services.


## List of Services


### Graph Generators

#### nx_graph_generator

Random graph generators using NetworkX's functions


### Graph Layouts

#### nx_layout

### Graph Analysis

## License

MIT

--------------------------------------------------------------------------------

## Contact

© 2017 University of California, San Diego Trey Ideker Lab
