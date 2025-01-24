# About
This repo contains the code to generate a static call graph for a given Github repository. The call graph is generated using the [pycg](!https://github.com/vitsalis/PyCG) tool, then visualized using [Pyvis](!https://github.com/WestHealth/pyvis). 

# Dependencies
```
poetry
```

## Poetry Setup
Run `poetry init` to initialize the virtual environment, then you can run the graph generation process by running `poetry run make`. 

[More on poetry](https://python-poetry.org/docs/managing-environments/)

# Steps to Generate Call Graph
```mermaid
   graph TD;
    A -->|Stores GitHub Repository Folder in ./libraries (Default Folder)| B
    B -->|Stores JSON-format Call Graph in ./cg_jsons (Default Folder)| C
    C -->|Stores HTML-Format Pyvis Call Graph in ./cg_htmls| D["Pipeline End"]
    A[call_graph/clone_github_repo.sh:<br />Clones Repository] 
    B[call_graph/generate_cg_json.sh:<br />Generate Static Call Graph JSON]
    C[call/graph/generate_call_graph.py<br />Produces Call Graph HTML] 
```
Default Folder paths can be modified in the Makefile script. For example:
```
    poetry run make CODE_FOLDER=./new_folder \
                    JSON_FOLDER=./another_folder \
                    HTML_FOLDER=./new_folder
```