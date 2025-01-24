# Define variables with comments
required_variables = ["function_name", "input_filename", "output_filename", "package_filter", "input_folder", "output_folder"] 

# Import necessary libraries
'''
    Author: Harris Zheng
    Date: July 13th, 2024

    Description: Generate a Code Call Graph from cg_json generates
                 from generate_call_graph.sh bash script
'''

## Important CG_json
import argparse
import re
import networkx as nx
import json
import os
from call_graph_functions import CallGraphCleaner
from pyvis.network import Network


PACKAGE_FILTER = "instaloader"
CG_JSON_FOLDER = "./cg_jsons/"
CG_JSON = "./cg_jsons/instaloader_cg.json"
CG_JSON = "./cg_jsons/instaloader_cg.json"  
OUTPUT_FOLDER_PATH = "./cg_htmls/"
OUTPUT_FILE_PATH = "./cg_htmls/instaloader_graph.html"


def main():
    '''
        1. Open the file.
        2. Filter on prefixes
        3. Add cg_json to PyVIS Network Graph
        4. Save HTML Visualization
    '''
    arg_parser = argparse.ArgumentParser(
        description="Script to convert cg_json into networkx graph"
    )
    # Add argument for cg_json file
    arg_parser.add_argument("-i", "--input_filename", required=True, type=str, help="Input cg_json filename")
    # Add argument for output file
    arg_parser.add_argument("-o", "--output_filename", required=True, type=str, help="Output html filename")
    
    # Add argument for package filter
    arg_parser.add_argument("-f", "--filter", required=True, type=str, help="Package filter")
    
    # Add argument for cg_json folder
    arg_parser.add_argument("--input_folder", type=str, help="Input cg_json folder", default=CG_JSON_FOLDER)
    # Add argument for output folder
    arg_parser.add_argument("--output_folder", type=str, help="Output html folder", default=OUTPUT_FOLDER_PATH)
    args = arg_parser.parse_args()
    
    # Set the input and output file paths
    input_file_path = os.path.join(args.input_folder, args.input_filename)    
    output_file_path = os.path.join(args.output_folder, args.output_filename)    
    package_filter = args.filter

    cg_class = CallGraphCleaner()

    # Load JSON graph in memory
    data = cg_class.load_json(input_file_path)
    new_json = cg_class.clean_json(data, package_filter)

    # Convert cg_json to NetworkX Graph
    network = cg_class.toNetwork(new_json)
    print("Number of Nodes:", len(network.nodes))
    print("Number of Edges:", len(network.edges))
    
    net = cg_class.ntw_pyvis(network)

    # Uncomment this line if you wish to debug the physics of your visualization
    # net.show_buttons(filter_=['physics'])
    
    # Save HTML Visualization
    _ = net.show(name=output_file_path)
    


if __name__ == "__main__":
    main()