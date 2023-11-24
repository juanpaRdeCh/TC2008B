from mesa import Agent
from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt
import random


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model, graph, moving=False):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = self.choose_random_destination()
        self.moving = moving
        self.graph = graph
        print("Destination:", self.destination.pos)
                

    def choose_random_destination(self):
        """
        Randomly choose a destination from the available destination agents.
        """
        destination_agents = [
            agent
            for agent in self.model.schedule.agents
            if isinstance(agent, Destination)
        ]
        if destination_agents:
            return random.choice(destination_agents)
        else:
            return None

    def move_to_destination(self):
        if self.destination is not None:
            current_position = self.pos
            destination_position = self.destination.pos
            
            try:
                path = nx.astar_path(self.graph, current_position, destination_position)
            except nx.NetworkXNoPath:
                print("No path found")
                return
            if path:
                new_position = path[1]
                self.model.grid.move_agent(self, new_position)
                
                if new_position == destination_position:
                    self.model.grid.move_agent(self, new_position)
                    self.model.schedule.remove(self)
                    self.model.grid.remove_agent(self)
                    print("Destination reached")
             


    def move(self):
        """
        Determines if the agent can move in the direction that was chosen.
        """
        self.move_to_destination()
        
    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.move()


class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """

    def __init__(self, unique_id, model, state=False, timeToChange=10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """

    def __init__(self, unique_id, model, direction):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
