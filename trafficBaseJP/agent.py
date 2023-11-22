from mesa import Agent
from queue import PriorityQueue
import networkx as nx
import random


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model, moving=False):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = self.choose_random_destination()
        self.moving = moving

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
        """
        Move the agent to its destination using A* pathfinding.
        """
        if self.destination is not None:
            current_position = self.pos
            destination_position = self.destination.pos

            # Create a graph from the grid
            G = nx.Graph()
            for x in range(self.model.width):
                for y in range(self.model.height):
                    if not any(
                        isinstance(agent, Obstacle)
                        for agent in self.model.grid.get_cell_list_contents((x, y))
                    ):
                        G.add_node((x, y))

            for edge in G.edges:
                G.edges[edge]["weight"] = 1

            # Find the shortest path using A*
            path = nx.astar_path(G, current_position, destination_position)

            if path:
                # Move to the next position in the path
                new_position = path[1]
                self.model.grid.move_agent(self, new_position)

    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )

        road_agents_around = [
            agent
            for agent in self.model.grid.get_neighbors(
                self.pos, moore=False, include_center=True
            )
            if isinstance(agent, Road)
        ]
        light_agents_around = [
            agent
            for agent in self.model.grid.get_neighbors(
                self.pos, moore=False, include_center=True
            )
            if isinstance(agent, Traffic_Light)
        ]

        road_positions = [agent.pos for agent in road_agents_around]
        road_direction = {agent.pos: agent.direction for agent in road_agents_around}

        current_direction = road_direction.get(road_positions[0], None)

        next_moves = [p for p in possible_steps if p in road_positions]

        print("Possible Steps:", possible_steps)
        print("Next Moves:", next_moves)

        if current_direction is not None:
            next_moves = [
                p for p in possible_steps if road_direction.get(p) == current_direction
            ]

            filtered_next_moves = [
                pos for pos in next_moves if road_direction[pos] == current_direction
            ]

            if filtered_next_moves:
                new_position = self.random.choice(filtered_next_moves)
                self.model.grid.move_agent(self, new_position)
                self.moving = True
        if light_agents_around:
            traffic_light = light_agents_around[0]
            if not traffic_light.state:
                self.moving = False
            else:
                if road_agents_around and filtered_next_moves:
                    new_position = self.random.choice(filtered_next_moves)
                    self.model.grid.move_agent(self, new_position)
                light_pos = traffic_light.pos
                self.model.grid.move_agent(self, light_pos)
                self.moving = True

        if self.destination is not None:
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

    def __init__(self, unique_id, model, direction="Left"):
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
