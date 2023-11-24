from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json


class CityModel(Model):
    """
    Creates a model based on a city map.

    Args:
        N: Number of agents in the simulation
    """

    def __init__(self, N):
        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []

        # Load the map file. The map file is a text file where each character represents an agent.
        with open("city_files/2022_base.txt") as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0]) - 1
            self.height = len(lines)
            
            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)

            corners = [
                (0, 0),
                (0, self.height - 1),
                (self.width - 1, 0),
                (self.width - 1, self.height - 1),
            ]


            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(
                            f"tl_{r*self.width+c}",
                            self,
                            False if col == "S" else True,
                            int(dataDictionary[col]),
                        )
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
            
            self.create_graph()

            for i, pos in enumerate(corners):
                Agent = Car(i + 1000, self, self.graph)
                self.schedule.add(Agent)
                self.grid.place_agent(Agent, pos)
               
        self.num_agents = N
        self.running = True
        
    def create_graph(self):
            """
            Create a graph from the grid with obstacles taken into account
            """
            G = nx.DiGraph()
            for x in range(self.width):
                for y in range(self.height):
                    cell_contents = self.grid.get_cell_list_contents((x, y))
                    if any(isinstance(agent, (Road, Traffic_Light, Destination)) for agent in cell_contents):
                        G.add_node((x, y))

            # Add edges to represent valid moves (considering obstacles)
            for x in range(self.width):
                for y in range(self.height):
                    cell_contents = self.grid.get_cell_list_contents((x, y))
                    if any(isinstance(agent, (Road, Traffic_Light, Destination)) for agent in cell_contents):
                        
                        current_node = (x, y)
                        neighbors = self.grid.get_neighborhood(
                            current_node, moore=False, include_center=False
                        )

                        for neighbor in neighbors:
                            neighbor_contents = self.grid.get_cell_list_contents(neighbor)
                            if any(isinstance(agent, (Road, Traffic_Light, Destination)) for agent in neighbor_contents):
                                current_agent = next(agent for agent in cell_contents if isinstance(agent, (Road, Traffic_Light, Destination))) #MOVE IT AFTER CURRENT_AGENT
                                
                                # G.add_edge(current_node, neighbor, weight=1)
                                if isinstance(current_agent, Road): #ADD CONDITION
                                    direction = current_agent.direction  # Fix this line
                                elif isinstance(current_agent, Traffic_Light):
                                    G.add_edge(current_node, neighbor, weight=1)
                                            
                                elif isinstance(current_agent, Destination):
                                    G.add_edge(neighbor, current_node, weight=1)
                                    
                                if direction == "Up" and y < neighbor[1]:
                                    G.add_edge(current_node, neighbor, weight=1)
                                elif direction == "Down" and y > neighbor[1]:
                                    G.add_edge(current_node, neighbor, weight=1)
                                elif direction == "Left" and x > neighbor[0]:
                                    G.add_edge(current_node, neighbor, weight=1)
                                elif direction == "Right" and x < neighbor[0]:
                                    G.add_edge(current_node, neighbor, weight=1)


            pos = {node: (node[0], node[1]) for node in G.nodes()}
            nx.draw(G, pos, with_labels=False, font_weight='bold')
            plt.show()
            self.graph = G
            
        
    def step(self):
        """Advance the model by one step."""
        
        self.schedule.step()

        # Create a new Car agent at each corner every 10 steps
        if self.schedule.steps % 10 == 0:
            corners = [
                (0, 0),
                (0, self.height - 1),
                (self.width - 1, 0),
                (self.width - 1, self.height - 1),
            ]
            for corner in corners:
                new_agent = Car(self.num_agents + 1, self, self.graph)
                self.num_agents += 1
                self.grid.place_agent(new_agent, corner)
                self.schedule.add(new_agent)
