from agent import Car, Traffic_Light, Destination, Obstacle, Road
from model import CityModel, cars, traffic_lights, destination, buidings, road
from flask import Flask, request, jsonify

app = Flask("Traffic Simulator")

@app.route('/init', methods=['GET','POST'])
def init_model():
    global cityModel, current_step, num_agents, width, height
    
    if request.method == "POST":
        map_path = request.form.get("MapPath")
        
        current_step = 0
         
        cityModel = CityModel(map_path)
         
        return jsonify({"message": "Model Initialized"})
    
@app.route('/getAgents', methods=['GET'])
def get_cars():
    global cityModel
    
    if request.method == 'GET':
        carData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0, "z":Agent.pos[1], "destination": Agent.destination}
                   for Agent in cars.values()]
        return jsonify({"cars": carData})

@app.route('/getRoads', methods=['GET'])
def get_roads():
    global cityModel
    
    if request.method == 'GET':
        roadData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0, "z":Agent.pos[1], "direction": Agent.direction}
                   for Agent in roads.values()]
        return jsonify({"roads": roadData})
        
@app.route('/getTrafficLights', methods=['GET'])
def get_traffic_lights():
    global cityModel
    
    if request.method == 'GET':
        trafficLightData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0, "z":Agent.pos[1], "state": Agent.state, "direction": Agent.direction}
                   for Agent in traffic_lights.values()]
        return jsonify({"trafficLights": trafficLightData})

@app.route('/getDestinations', methods=['GET'])
def get_destinations():
    global cityModel
    
    if request.method == 'GET':
        destinationData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0, "z":Agent.pos[1]}
                   for Agent in destination.values()]
        return jsonify({"destinations": destinationData})
        
@app.route('/getObstacles', methods=['GET'])
def get_obstacles():
    global cityModel
    
    if request.method == 'GET':
        obstacleData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0, "z":Agent.pos[1]}
                   for Agent in buidings.values()]
        return jsonify({"obstacles": obstacleData})

@app.route('/update', methods=['GET'])
def updateModel():
    global cityModel, current_step
    
    if request.method == 'GET':
        cityModel.step()
        current_step += 1
        return jsonify({"message": "Model Updated"})

if __name__ == "__main__":
    app.run(host="localhost", port=8585, debug=True)
     