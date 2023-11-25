/*
TC2008B. Sistemas Multiagentes y Gráficas Computacionales
AgentController.cs | 2023
David Flores Becerril
Juan Pablo Ruiz de Chavez Diez de Urdanivia

Script que controla el comportamiento de los agentes en la escena.
*/

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEngine.Networking;

[Serializable]
public class AgentData{
    //Contains AgentData

    public string id;
    public float x,y,z;

    public AgentData(string id, float x, float y, float z){
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]

public class RoadData : AgentData{
    //Contains RoadData

    public string direction;

    public RoadData(string id, float x, float y, float z) : base(id, x, y, z){
        this.direction = direction;
    }

}


[Serializable]
public class TrafficLightData : RoadData{
    //Contains TrafficLightData

    public string state;

    public TrafficLightData(string id, float x, float y, float z, string state) : base(id, x, y, z){
        this.state = state;
    }
}

[Serializable]
public class CarData : AgentData{
    //Contains CarData

    public string destination;

    public CarData(string id, float x, float y, float z, string direction, string state) : base(id, x, y, z){
        this.destination = destination;
    }
}

//Clases de la lista de agentes
[Serializable]
public class AgentsData{

    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
    
}

[Serializable]
public class RoadsData{

    public List<RoadData> data;

    public RoadsData() => this.data = new List<RoadData>();
    
}

[Serializable]
public class TrafficLightsData{

    public List<TrafficLightData> data;

    public TrafficLightsData() => this.data = new List<TrafficLightData>();
    
}

[Serializable]
public class CarsData{

    public List<CarData> data;

    public CarsData() => this.data = new List<CarData>();
    
}


public class AgentController : MonoBehaviour {
    string serverUrl = "http://localhost:8585";
    string getCarsEndpoint = "/getAgents";
    string getRoadEndpoint = "/getRoads";
    string getTrafficLightsEndpoint = "/getTrafficLights";
    string getDestinationsEndpoint = "/getDestinations";
    string getBuildingsEndpoint = "/getObstacles";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";

    CarsData carsData;
    RoadsData roadsData;
    TrafficLightsData trafficLightsData;
    AgentsData buildingData;
    AgentsData destinationsData;

    Dictionary<string, GameObject> roads, cars, tLights, destinations, buildings;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, roadsStarted = false, carsStarted = false, tLightsStarted = false, destinationsStarted = false, buildingsStarted = false;

    public GameObject roadPrefab, tLightsPrefab;

    public GameObject[] carPrefabsVariant, destinationsPrefabsVariant, buildingsPrefabsVariant;

    public string MapPath = "Assets/Data/2022_prueba.txt";

    public float timeToUpdate = 5.0f;

    private float timer, dt;

    private int carsSpawned, arrivals;

    void Start(){
        roadsData = new RoadsData();
        carsData = new CarsData();
        trafficLightsData = new TrafficLightsData();
        buildingData = new AgentsData();
        destinationsData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        roads = new Dictionary<string, GameObject>();
        cars = new Dictionary<string, GameObject>();
        tLights = new Dictionary<string, GameObject>();
        destinations = new Dictionary<string, GameObject>();
        buildings = new Dictionary<string, GameObject>();

        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());

    }

    private void Update() {
        if(timer < 0){
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated){
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach (var car in currPositions){
                Vector3 currentPositions = car.Value;
                Vector3 previousPositions = prevPositions[car.Key];

                Vector3 interpolated = Vector3.Lerp(previousPositions, currentPositions, dt);
                Vector3 direction = currentPositions - interpolated;

                cars[car.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero){
                    cars[car.Key].transform.rotation = Quaternion.LookRotation(direction);
                }
            }
        }

        IEnumerator UpdateSimulation(){
            UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
            yield return www.SendWebRequest();


            if (www.result != UnityWebRequest.Result.Success){
                Debug.Log(www.error);
            }
            else{
                StartCoroutine(GetCarsData());
                StartCoroutine(GetTrafficLightsData());

            }
        
        }

        IEnumerator SendConfiguration(){
            WWWForm form = new WWWForm();

            form.AddField("MapPath", MapPath.ToString());

            UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
            www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success){
                Debug.Log(www.error);
            }
            else{
                StartCoroutine(GetRoadsData());
                StartCoroutine(GetTrafficLightsData());
                StartCoroutine(GetCarsData());
                StartCoroutine(GetDestinationsData());
                StartCoroutine(GetBuildingsData());
            }

        }

        IEnumerator GetRoadsData(){
            UnityWebRequest www = UnityWebRequest.Get(serverUrl + getRoadEndpoint);
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success){
                Debug.Log(www.error);
            }
            else{

                roadsData = JsonUtility.FromJson<RoadsData>(www.downloadHandler.text);

                foreach (RoadData road in roadsData.data){
                    if(!roadsStarted){
                        roads[road.id] = Instantiate(roadPrefab, new Vector3(road.x, road.y, road.z), Quaternion.identity);
                        if(road.direction == "Up" || road.direction == "Down"){
                            roads[road.id].transform.Rotate(0, 90, 0);
                        }
                    }
                }
                updated = true;
                if(!roadsStarted){
                    roadsStarted = true;
                }
            }
        }

        IEnumerator GetCarsData(){
            UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success){
                Debug.Log(www.error);
            }
            else{
                
                carsSpawned = 0;
                carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

                foreach (CarData car in carsData.data){
                    if(!carsStarted){
                        cars[car.id] = Instantiate(carPrefabsVariant[UnityEngine.Random.Range(0, carPrefabsVariant.Length)], new Vector3(car.x, car.y, car.z), Quaternion.identity);
                        cars[car.id].transform.parent = GameObject.Find("Cars").transform;
                        carsSpawned++;
                    }
                    prevPositions[car.id] = new Vector3(car.x, car.y, car.z);
                    currPositions[car.id] = new Vector3(car.x, car.y, car.z);
                }
                updated = true;
                if(!carsStarted){
                    carsStarted = true;
                }
            }
        }
        



    }



}