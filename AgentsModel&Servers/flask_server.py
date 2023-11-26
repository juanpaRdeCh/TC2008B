from agent import Car, Traffic_Light, Destination, Obstacle, Road
from model import CityModel, cars, traffic_lights, destination, buidings, road
from flask import Flask, request, jsonify

app = Flask("Traffic Simulator")

@app.route('/init', methods=['GET','POST'])
def init_model():
    global cityModel, current_step, num_agents, width, height
    
    if request.method == 'POST':
        
        map_path = request.form.get('MapPath')
        
        current_step = 0
        
        cityModel = CityModel(map_path)
         
        return jsonify({"message": "Model Initialized"})
        
@app.route('/getAgents', methods=['GET'])
def get_cars():
    global cityModel
    
    if request.method == 'GET':
        carData = [{"id": str(Agent.unique_id), "x": Agent.pos[0], "y": 0.169, "z":Agent.pos[1], "destination": Agent.destination.pos}
                   for Agent in cars.values()]
        return jsonify({"data": carData})

@app.route('/getRoads', methods=['GET'])
def get_roads():
    global cityModel
    
    if request.method == 'GET':
        roadData = [{"id": str(road.unique_id), "x": road.pos[0], "y": 0, "z":road.pos[1], "direction": road.direction}
                   for road in road.values()]
        return jsonify({"data": roadData})
        

@app.route('/getTrafficLights', methods=['GET'])
def get_traffic_lights():
    global cityModel
    
    if request.method == 'GET':
        trafficLightPositions = [{"id": str(tls.unique_id), "x": tls.pos[0], "y": 0.7, "z":tls.pos[1], "state": tls.state}
                   for tls in traffic_lights.values()]
        return jsonify({"data": trafficLightPositions})

@app.route('/getDestinations', methods=['GET'])
def get_destinations():
    global cityModel
    
    if request.method == 'GET':
        destinationPositions = [{"id": str(des.unique_id), "x": des.pos[0], "y": 0.01, "z":des.pos[1]}
                   for des in destination.values()]
        return jsonify({"positions": destinationPositions})
        
@app.route('/getObstacles', methods=['GET'])
def get_obstacles():
    global cityModel
    
    if request.method == 'GET':
        obstaclePositions = [{"id": str(obs.unique_id), "x": obs.pos[0], "y": 0.01, "z":obs.pos[1]}
                   for obs in buidings.values()]
        return jsonify({"positions": obstaclePositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global cityModel, current_step
    
    if request.method == 'GET':
        cityModel.step()
        current_step += 1
        return jsonify({"message": "Model Updated"})

if __name__ == "__main__":
    app.run(host="localhost", port=8585, debug=True)
     