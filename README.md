# About
This repo contains the code to generate a static call graph for a given Github repository. The call graph is generated using the [pycg](!https://github.com/vitsalis/PyCG) tool, then visualized using [Pyvis](!https://github.com/WestHealth/pyvis). 

# Dependencies
Make sure you have aws cli installed: https://aws.amazon.com/cli/

# Steps to Generate Call Graph

1. git clone repo
2. run pycg command and use bash to filter for interested entrypoints.
3. run generate_call_graph.ipynb with the correct parameters for resulting call graph