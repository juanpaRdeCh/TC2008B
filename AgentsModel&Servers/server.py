#Script para correr el modelo mediante una visualización de mesa 


from agent import *
from model import CityModel
from mesa.visualization import CanvasGrid
from mesa.visualization.modules import TextElement
from mesa.visualization import ModularServer


class CarCount(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return f"Car Count: {model.car_count()}"


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 1, "w": 1, "h": 1}

    if isinstance(agent, Road):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0

    if isinstance(agent, Destination):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if isinstance(agent, Traffic_Light):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if isinstance(agent, Obstacle):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    if isinstance(agent, Car):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 2
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal


width = 0
height = 0

with open("city_files/2023_base.txt") as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0]) - 1
    height = len(lines)

model_params = {"map_path": "/city_files/2023_base.txt"}

grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
car_count = CarCount()

server = ModularServer(CityModel, [grid, car_count], "Traffic Base", model_params)
server.port = 8522  # The default
server.launch()
