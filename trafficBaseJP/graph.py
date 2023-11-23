from mesa import Model, agent
import networkx as nx
import matplotlib.pyplot as plt

class CityModel(Model):
def create_graph(model):
    """
    Create a graph from the grid with obstacles taken into account
    """
    G = nx.DiGraph()
    grid_map = [
        "v<<<<<<<<<<<<<<<<<s<<<<<<",
        "v<<<<<<<<<<<<<<<<<s<<<<^",
        "vv#D#########vv#SS###D^^",
        "vv###########vv#^^####^^",
        "vv##########Dvv#^^D###^^",
        "vv#D#########vv#^^####^^",
        "vv<<<<<<s<<<<vv#^^####^^",
        "vv<<<<<<s<<<<vv#^^####^^",
        "vv####SS#####vv#^^####^^",
        "vvD##D^^####Dvv#^^####^^",
        "vv####^^#####vv#^^D###^^",
        "SS####^^#####vv#^^####^^",
        "vvs<<<<<<<<<<<<<<<<<<<<<",
        "vvs<<<<<<<<<<<<<<<<<<<<<",
        "vv##########vv###^^###^^",
        "vv>>>>>>>>>>>>>>>>>>>s^^",
        "vv>>>>>>>>>>>>>>>>>>>s^^",
        "vv####vv##D##vv#^^####SS",
        "vv####vv#####vv#^^####^^",
        "vv####vv#####vv#^^###D^^",
        "vv###Dvv####Dvv#^^####^^",
        "vv####vv#####vv#^^####^^",
        "vv####SS#####SS#^^#D##^^",
        "v>>>>s>>>>>>s>>>>>>>>>>^",
        ">>>>>s>>>>>>s>>>>>>>>>>^"
    ]

    for x, row in enumerate(grid_map):
        for y, cell in enumerate(row):
            if cell == "#":
                continue  # Skip obstacles
            G.add_node((x, y))

            if cell == "D":
                # Add an edge from the current node to the destination (D)
                destination_pos = (0, 0)  # Replace with the actual position of the destination
                G.add_edge((x, y), destination_pos)

            # Define the valid moves based on the specified directions
            directions = {"v": (0, -1), ">": (1, 0), "^": (0, 1), "<": (-1, 0)}

            for direction, (dx, dy) in directions.items():  # Change nx to dx
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid_map) and 0 <= ny < len(grid_map[0]) and grid_map[nx][ny] not in {"#", "s", "S"}:
                    G.add_edge((x, y), (nx, ny), weight=1)

    pos = {node: node for node in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    plt.show()
    return G

# Run the function with a dummy model
create_graph(CityModel)
