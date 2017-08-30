# graph-tool Service Example

## Introduction
graph-tool is a high-performance graph library using Boost Graph.  This is an example service to perform layout using graph-tool.

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
