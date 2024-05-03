# CS162 Solo Project: Bus Network Analysis
See the [full report](./CS162_Project_Report.pdf).
Below are the tasks of each week with their corresponding module.

## Week 03
### 1. Appendix I.1, Create a private GitHub repository
### 2. Appendix I.2, Clone a repository from GitHub
### 3. Appendix I.3, Create new files and folders in GitHub
### 4. Appendix I.4, `.gitignore` 101
### 5. Appendix I.5, Basic Git commands (add, commit, push, pull)
### 6. Appendix II.1, Python project with multiple files
### 7. Appendix II.2, Importing external files
### 8. Appendix II.3, Python classes, properties and methods

## Week 05
### 1. Section 5.1, `Stop`; Subsection 10.2.1, `StopQuery`
* [Module `elements.stop`](./elements/stop/)
* [Module `queries.StopQuery`](./queries/stop_query/)

### 2. Section 5.2, `Variant`; Subsection 10.2.2, `VariantQuery`
* [Module `elements.variant`](./elements/variant/)
* [Module `queries.VariantQuery`](./queries/variant_query/)

### 3. Section 10, Querying List of Objects
## Week 06
### 1. Chapter 1, PROJ: Coordinate Transformation
### 2. Chapter 2, GeoJSON: Geosptial Data Format
### 3. Section 5.3, `Path`; Subsection 10.2.3, `PathQuery`
* [Module `elements.path`](./elements/path/)
* [Module `queries.PathQuery`](./queries/path_query/)
### 4. Chapter 3, Shapely: Spatial Analysis
### 5. Chapter 4, R-tree: Data Structure for Spatial Data
### 6. Section 11.1, Querying a `pandas.DataFrame`
* [Jupyter notebook `llm_test.ipynb`](./llm_test.ipynb)

## Week 07
### 1. Chapter 6, Bus Network Graph: Construction Stage
* [Module `network`](./network/)
* [Module `network.bus`](./network/bus/)

### 2. Chapter 7, Dijkstra: Shortest Paths and related Centrality Measures
* [Module `network.shortest_paths.dijkstra`](./network/shortest_paths/dijkstra.py)

### 3. Section 7.2, APSP: All Pairs Shortest Path problem

### 4. Section 7.3, Betweenness Centrality; Section 9.1.3, `NetworkAnalysisBetweenness` class
* [Module `network.shortest_paths.betweenness`](./network/shortest_paths/betweenness.py)

## Week 10
### 1. Chapter 8, Space-efficient Shortest Path Querying: Bidirectional Dijkstra, Contraction Hierarchy
* [Module `network.shortest_paths.bidirectional_dijkstra`](./network/shortest_paths/bidirectional_dijkstra.py)

* [Module `network.shortest_paths.contraction_hierarchies`](./network/shortest_paths/contraction_hierarchies)

### 2. Section 9.3, Experiments on real data
* [Jupyter notebook `main.ipynb`](./main.ipynb)

## Week 11
### Chapter 11, LangChain: Apply Large Language Model to Querying Databases
* [Jupyter notebook `llm-test.ipynb`](./llm-test.ipynb)