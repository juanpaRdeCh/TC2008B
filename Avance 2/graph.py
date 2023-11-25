import networkx as nx
import matplotlib.pyplot as plt

# Data mapping symbols to their meanings
symbol_mapping = {
    ">" : "Right",
    "<" : "Left",
    "S" : 15,
    "s" : 7,
    "#" : "Obstacle",
    "v" : "Down",
    "^" : "Up",
    "D" : "Destination"
}

# Given map
city_map = """
v<<<<<<<<<<<<<<<<<s<<<<<
v<<<<<<<<<<<<<<<<<s<<<<^
vv#D#########vv#SS###D^^
vv###########vv#^^####^^
vv##########Dvv#^^D###^^
vv#D#########vv#^^####^^
vv<<<<<<s<<<<vv#^^####^^
vv<<<<<<s<<<<vv#^^####^^
vv####SS#####vv#^^####^^
vvD##D^^####Dvv#^^####^^
vv####^^#####vv#^^D###^^
SS####^^#####vv#^^####^^
vvs<<<<<<<<<<<<<<<<<<<<<
vvs<<<<<<<<<<<<<<<<<<<<<
vv##########vv###^^###^^
vv>>>>>>>>>>>>>>>>>>>s^^
vv>>>>>>>>>>>>>>>>>>>s^^
vv####vv##D##vv#^^####SS
vv####vv#####vv#^^####^^
vv####vv#####vv#^^###D^^
vv###Dvv####Dvv#^^####^^
vv####vv#####vv#^^####^^
vv####SS#####SS#^^#D##^^
v>>>>s>>>>>>s>>>>>>>>>>^
>>>>>s>>>>>>s>>>>>>>>>>^
"""

# Convert the map into a list of lists
city_map_lines = [list(line.strip()) for line in city_map.strip().split('\n')]

# Create a directed graph
city_graph = nx.DiGraph()

# Iterate through the map and add nodes and edges to the graph
for i in range(len(city_map_lines)):
    for j in range(len(city_map_lines[i])):
        symbol = city_map_lines[i][j]
        if symbol in ('<', '>', 'v', '^', 'D', 's', 'S'):
            city_graph.add_node((i, j), type=symbol_mapping[symbol])

            # Add edges based on the direction of the streets
            if symbol in ('<', '>', 'v', '^'):
                if symbol == '<' and j > 0 and city_map_lines[i][j - 1] in ('<', '>'):
                    city_graph.add_edge((i, j), (i, j - 1))
                elif symbol == '>' and j < len(city_map_lines[i]) - 1 and city_map_lines[i][j + 1] in ('<', '>'):
                    city_graph.add_edge((i, j), (i, j + 1))
                elif symbol == '^' and i > 0 and city_map_lines[i - 1][j] in ('^', 'v'):
                    city_graph.add_edge((i, j), (i - 1, j))
                elif symbol == 'v' and i < len(city_map_lines) - 1 and city_map_lines[i + 1][j] in ('^', 'v'):
                    city_graph.add_edge((i, j), (i + 1, j))

# Visualize the graph (optional)
pos = dict((node, node) for node in city_graph.nodes())
nx.draw(city_graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', arrowsize=20)
plt.show()