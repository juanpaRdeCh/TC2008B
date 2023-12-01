#Scrip que contiene el comportamiento de cada agente para el modelo de mesa

from mesa import Agent
from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


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
        self.path_calculated = False
        self.path = None

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
            if self.trafficlightstate() and self.avoid_car_collision():
                current_position = self.pos
                destination_position = self.destination.pos

                try:
                    path = nx.astar_path(
                        self.graph, current_position, destination_position
                    )
                except nx.NetworkXNoPath:
                    print("No path found")
                    return
                if path:
                    new_position = path[1]
                    self.model.grid.move_agent(self, new_position)

                    if new_position == destination_position:
                        self.model.schedule.remove(self)
                        self.model.grid.remove_agent(self)
                        self.model.cars.pop(self.unique_id)
                        self.model.agents_arrived += 1
        else:
            self.moving = False

    # Intento de move to destination con paciencia
    def move_to_destination2(self):
        if self.destination is not None:
            if self.trafficlightstate() and self.avoid_car_collision2():
                current_position = self.pos
                destination_position = self.destination.pos

                if not self.path_calculated:
                    try:
                        self.path = nx.astar_path(
                            self.graph, current_position, destination_position
                        )
                        self.path_calculated = True
                    except nx.NetworkXNoPath:
                        print("No path found")
                        self.path_calculated = False
                        return
                if self.avoid_car_collision2() and self.recalculate_path():
                    try:
                        self.path = nx.astar_path(
                            self.graph, current_position, destination_position
                        )
                    except nx.NetworkXNoPath:
                        print("No path found")
                        return
                if self.path:
                    new_position = self.path[1]
                    self.model.grid.move_agent(self, new_position)

                    if new_position == destination_position:
                        self.model.schedule.remove(self)
                        self.model.grid.remove_agent(self)
                        self.model.cars.pop(self.unique_id)
                        self.model.agents_arrived += 1
        else:
            self.moving = False

    def avoid_car_collision(self):
        """
        Determines if there is a car in the current direction of movement. If there is, the car agent stops until the car in front moves.
        """
        x, y = self.pos
        current_node = (x, y)

        # Obtener la próxima posición del agente
        next_position = self.get_next_position()

        # Calcular la dirección de movimiento
        direction_of_movement = (next_position[0] - x, next_position[1] - y)

        # Obtener el vecino en la dirección de movimiento
        neighbor = (x + direction_of_movement[0], y + direction_of_movement[1])

        # Verificar si hay un coche en la dirección de movimiento
        neighbor_agent = self.model.grid.get_cell_list_contents([neighbor])
        for agent in neighbor_agent:
            if isinstance(agent, Car):
                return False
        return True

    def avoid_car_collision2(self):
        """
        Determines if there is a car in the current direction of movement. If there is, the car agent stops until the car in front moves.
        """
        x, y = self.pos
        current_node = (x, y)

        # Obtener la próxima posición del agente
        next_position = self.get_next_position()

        # Calcular la dirección de movimiento
        direction_of_movement = (next_position[0] - x, next_position[1] - y)

        # Obtener el vecino en la dirección de movimiento
        neighbor = (x + direction_of_movement[0], y + direction_of_movement[1])

        # Verificar si hay un coche en la dirección de movimiento
        neighbor_agent = self.model.grid.get_cell_list_contents([neighbor])
        for agent in neighbor_agent:
            if isinstance(agent, Car):
                self.recalculate_path()
                return False
        return True

    def recalculate_path(self):
        recaltulate = random.randint(1, 10)
        if recaltulate == 1:
            return False
        elif recaltulate == 2:
            return True
        elif recaltulate == 3:
            return True
        elif recaltulate == 4:
            return False
        elif recaltulate == 5:
            return False
        elif recaltulate == 6:
            return False
        elif recaltulate == 7:
            return False
        elif recaltulate == 8:
            return False
        elif recaltulate == 9:
            return False
        elif recaltulate == 10:
            return False

    def trafficlightstate(self):
        """
        Determines if the car agent has a neighbor traffic light. If the neighbor traffic light is red, the car agent stops until
        the traffic light is green. If there is no neighbor traffic light, the car agent continues moving.
        """
        x, y = self.pos
        current_node = (x, y)

        # Obtener la próxima posición del agente
        next_position = self.get_next_position()

        # Calcular la dirección de movimiento
        direction_of_movement = (next_position[0] - x, next_position[1] - y)

        # Obtener el vecino en la dirección de movimiento
        neighbor = (x + direction_of_movement[0], y + direction_of_movement[1])

        # Verificar si hay un semáforo en la dirección de movimiento
        neighbor_agent = self.model.grid.get_cell_list_contents([neighbor])
        for agent in neighbor_agent:
            if isinstance(agent, Traffic_Light):
                if agent.state == False:
                    return False
                else:
                    return True
        return True

    def get_next_position(self):
        """
        Get the next position the car is planning to move to.
        """
        current_position = self.pos
        destination_position = self.destination.pos

        try:
            path = nx.astar_path(self.graph, current_position, destination_position)
            if len(path) > 1:
                return path[1]
            else:
                return current_position
        except nx.NetworkXNoPath:
            print("No path found")
            return current_position

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

    def __init__(self, unique_id, model, state=False, timeToChange=10, direction=None):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.direction = direction
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
