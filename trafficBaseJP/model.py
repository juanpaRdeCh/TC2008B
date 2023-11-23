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

            for i, pos in enumerate(corners):
                Agent = Car(i + 1000, self)
                self.schedule.add(Agent)
                self.grid.place_agent(Agent, pos)
                
                
        self.num_agents = N
        self.running = True

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
                new_agent = Car(self.num_agents + 1, self)
                self.num_agents += 1
                self.grid.place_agent(new_agent, corner)
                self.schedule.add(new_agent)
