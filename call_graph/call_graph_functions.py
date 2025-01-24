import re
import json
import numpy as np
import networkx as nx
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import Normalize,  LinearSegmentedColormap
import pyvis

class CallGraphCleaner:
    def __init__(self):
        pass

    def load_json(self, file_path: str) -> dict:
        '''
        Load JSON file from the given file path.
        
        :param file_path: Path to the JSON file
        :return: Loaded dictionary from the JSON file
        '''
        with open(file_path, 'r') as file:
            return json.load(file)


    def clean_json(self, dictionary: dict, package_filter: str) -> dict:
        '''
        Change the format of all file paths to standard package naming convention in Python
        and build network graph.

        :param dictionary: Input dictionary
        :param package_filter: Filter string for packages
        :return: Cleaned dictionary with modified file paths
        '''
        new_dict = {}
        for key, value in dictionary.items():
            new_key = re.sub(r"[\\]+", ".", key.strip(".\\"))  # Strip characters and replace slashes
            new_values = [re.sub(r"[\\]+", ".", elm.strip(".\\")) for elm in value] # Strip characters and replace slashes

            # Only consider related packages in "from" node
            if not re.match(package_filter, new_key):
                continue

            # Only consider related packages in "to" node
            new_values = list(filter(lambda x: re.match(package_filter, x), new_values))
        
            if new_key in new_dict:
                new_dict[new_key].extend(new_values)
            else:
                new_dict[new_key] = new_values
        
        assert len(new_dict) != 0, "Graph should not be empty"
        return new_dict

    def toNetwork(self, data: dict)->  nx.DiGraph:
        '''
            Convert the dictionary to a network graph using NetworkX library.
            
            :param data: Input dictionary
            :return: NetworkX DiGraph object
        '''
        nt = nx.DiGraph()

        def checkKey(name):
            if name not in nt:
                nt.add_node(name, size=40)

        for node in data:
            checkKey(node)
            for child in data[node]:
                checkKey(child)
                nt.add_edge(node,child)
        return nt   
    
    def configure_color_encodings(self, color_scheme="RdBu", minValue=-1, maxValue=1)-> nx.DiGraph:
        '''
            Configure color encodings for the network graph based on a given color map.
            The color encoding is based on the number of incoming and outgoing edges for each node,
            determined by the difference between outgoing edges to incoming edges:
                difference = outgoing edges - incoming_edges

            If the difference is greater than 0, the node is colored blue, otherwise it is colored red 
            (based on default colormap).

            Color intensity grows with rising values above 0 and decreasing values below 0.
            
            The size encoding of the node is determined by the same difference value and behaves similarly as color encoding, 
            but is scaled differently.

            :param ntx: Input NetworkX DiGraph object
            :param color_scheme: Color map scheme to use for color encoding. Default is "RdBu"

            :return: NetworkX DiGraph object with color encodings configured
        '''
        
        pass

    def ntw_pyvis(self, ntx:nx.DiGraph):
        '''
            Convert the network graph to a Pyvis network graph for visualization.
            
            :param ntx: Input NetworkX DiGraph object
            :return: Pyvis network graph object
        '''

        def convert_rgb_to_hex(rgb_color : tuple) -> str:
            '''
            Convert an RGB color tuple to a hexadecimal color string.

            :param rgb_color: RGB color tuple (r, g, b) where r, g, b are in the range [0, 255] or [0, 1] if normalized
            :return: Hexadecimal color string in the format "#RRGGBB" where RR, GG, and BB are hexadecimal values representing the red, green, and blue components of the color, respectively
            '''

            # Normalize RGB values to the range [0, 1] if they are in the range [0, 255]
            normalized_rgb = tuple(val / 255 if val > 1 else val for val in rgb_color)

            # Convert normalized RGB values to hexadecimal values
            hex_color = f"#{int(normalized_rgb[0] * 255):02x}{int(normalized_rgb[1] * 255):02x}{int(normalized_rgb[2] * 255):02x}"
            
            return hex_color

        net = pyvis.network.Network(width="100%",height="1000px", directed=True, notebook=True,
                    cdn_resources='remote', select_menu=True, filter_menu=True)
        
        incoming_counts = {node: ntx.in_degree(node) for node in ntx.nodes()}
        outgoing_counts = {node: ntx.out_degree(node) for node in ntx.nodes()}
        
        # Normalize values from 0 to 1
        # difference_norm = Normalize(vmin=-max(incoming_counts.values()), vmax=max(outgoing_counts.values()))
        sum_norm = Normalize(
            vmin=min(list(incoming_counts.values()) + list(outgoing_counts.values())), 
            vmax=max(incoming_counts.values()) + max(outgoing_counts.values())
        )

        # Create custom RdBu colormap ignoring extremely high values
        # colors = mpl.colormaps["RdBu"](np.linspace(0, 1, 100))
        # colormap = LinearSegmentedColormap.from_list('custom_RdBu', colors)

        for node in ntx.nodes:
            incoming_count = incoming_counts[node]
            outgoing_count = outgoing_counts[node]
            
            # Calculate the difference between outgoing and incoming edges
            # difference = outgoing_count - incoming_count
            sum_of_counts = outgoing_count + incoming_count

            # Normalize the difference value to the range [0, 1] for color mapping, then convert rgb color to hex
            # normalized_difference = difference_norm(difference)
            # rgb_color_to_use = colormap(normalized_difference)
            # hex_color_to_use = convert_rgb_to_hex(rgb_color_to_use)

            # Shape encoding
            normalized_sum = sum_norm(sum_of_counts)
            size = normalized_sum * 4 + 16 # Range (16 to 20)

            net.add_node(node, **{"label":node, "value" : size})

        for edge in ntx.edges:
            net.add_edge(edge[0], edge[1], width=1)

        # Configure options for the network layout
        '''
            Smaller spring length
            Smaller spring constant, once again for more natural graph movement
            Less damping to make the network graph's movements more natural
            More overlap avoidance
            Minimum velocity of 0.75
        '''
        options = """
        const options = {
            "physics": {
                "barnesHut": {
                "springLength": 70,
                "springConstant": 0.01,
                "damping": 0.06,
                "avoidOverlap": 0.16
                },
                "minVelocity": 0.75
            }
        }
        """
        net.set_options(options)
        return net     
