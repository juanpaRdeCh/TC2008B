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
    //Contains AgentData for each agent

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

    public RoadData(string id, float x, float y, float z, string direction) : base(id, x, y, z){
        this.direction = direction;
    }

}


[Serializable]
public class TLightData : AgentData{
    //Contains TrafficLightData

    public bool state;

    public TLightData(string id, float x, float y, float z, bool state) : base(id, x, y, z){
        this.state = state;
    }
}

[Serializable]
public class CarData : AgentData{
    //Contains CarData

    public string destination;

    public CarData(string id, float x, float y, float z, string destination) : base(id, x, y, z){
        this.destination = destination;
    }
}

//Contains data of every all agents
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
public class TLightsData{

    public List<TLightData> data;

    public TLightsData() => this.data = new List<TLightData>();
    
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
    TLightsData trafficLightsData;
    AgentsData buildingData;
    AgentsData destinationsData;

    Dictionary<string, GameObject> roads, cars, tLights, destinations, buildings;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, roadsStarted = false, carsStarted = false, tLightsStarted = false, destinationsStarted = false, buildingsStarted = false;

    public GameObject roadPrefab, tLightsPrefab;

    public GameObject[] carPrefabsVariant, destinationsPrefabsVariant, buildingsPrefabsVariant;

    public string MapPath = "../AgentsModel&Servers/city_files/2022_prueba.txt";

    public float timeToUpdate = 5.0f;

    private float timer, dt;

    private int carsSpawned, arrivals;

    void Start(){
        roadsData = new RoadsData();
        carsData = new CarsData();
        trafficLightsData = new TLightsData();
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

    private void Update(){
        if(timer < 0){
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated){
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach (var car in currPositions){
                Vector3 currentPosition = car.Value;
                Vector3 previousPosition = prevPositions[car.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                cars[car.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero){
                    cars[car.Key].transform.rotation = Quaternion.LookRotation(direction);
                }
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
            StartCoroutine(GetTLightsData());
            Debug.Log("Simulation Updated");
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
            StartCoroutine(GetTLightsData());
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
            string jsonData = www.downloadHandler.text;

            Debug.Log("Received Roads Data: " + jsonData);

            roadsData = JsonUtility.FromJson<RoadsData>(jsonData);

            foreach (RoadData road in roadsData.data){
                if(!roadsStarted){
                    roads[road.id] = Instantiate(roadPrefab, new Vector3(road.x, road.y, road.z), Quaternion.identity);
                    if(road.direction == "Left" || road.direction == "Right"){
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

    IEnumerator GetCarsData(){ //Work in progress
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else{
            
            carsSpawned = 0;
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

            foreach (CarData car in carsData.data){
                Vector3 newCarPosition = new Vector3(car.x, car.y, car.z);

                if(!carsStarted){
                    prevPositions[car.id] = newCarPosition;
                    GameObject carPrefab = carPrefabsVariant[UnityEngine.Random.Range(0, carPrefabsVariant.Length)];
                    cars[car.id] = Instantiate(carPrefab, newCarPosition, Quaternion.identity);
                }
                else{
                    Vector3 currentPosition = new Vector3();

                    if(!cars.ContainsKey(car.id)){
                        prevPositions[car.id] = newCarPosition;
                        GameObject carPrefab = carPrefabsVariant[UnityEngine.Random.Range(0, carPrefabsVariant.Length)];
                        cars[car.id] = Instantiate(carPrefab, newCarPosition, Quaternion.identity);
                    }

                    if (currPositions.TryGetValue(car.id, out currentPosition)){
                        prevPositions[car.id] = currentPosition;
                    }
                    currPositions[car.id] = newCarPosition;

                }

                carsSpawned++;
            }
            Debug.Log("Cars Spawned: " + carsSpawned);

            updated = true;
            if(!carsStarted){
                carsStarted = true;
            }
        }
    }

    IEnumerator GetTLightsData(){ //Work in progress
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLightsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else{
            trafficLightsData = JsonUtility.FromJson<TLightsData>(www.downloadHandler.text);

            foreach (TLightData tLight in trafficLightsData.data){
                if(!tLightsStarted){
                    tLights[tLight.id] = Instantiate(roadPrefab, new Vector3(tLight.x, tLight.y = 0, tLight.z), Quaternion.identity);
                    tLights[tLight.id] = Instantiate(tLightsPrefab, new Vector3(tLight.x, tLight.y, tLight.z), Quaternion.identity);
                }
                else{
                    if(tLight.state){
                        tLights[tLight.id].GetComponent<Renderer>().material.color = Color.green;
                    }
                    else{
                        tLights[tLight.id].GetComponent<Renderer>().material.color = Color.red;
                    }
                }
                
                
            }
            updated = true;
            if(!tLightsStarted){
                tLightsStarted = true;
            }
        }
    }


    IEnumerator GetDestinationsData(){
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getDestinationsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else{
            destinationsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData destination in destinationsData.positions){
                if(!destinationsStarted){
                    GameObject destinationPrefab = destinationsPrefabsVariant[UnityEngine.Random.Range(0, destinationsPrefabsVariant.Length)];
                    destinations[destination.id] = Instantiate(destinationPrefab, new Vector3(destination.x, destination.y, destination.z), Quaternion.identity);
                }
            }
            updated = true;
            if(!destinationsStarted){
                destinationsStarted = true;
            }
        }
    }

    IEnumerator GetBuildingsData(){
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBuildingsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success){
            Debug.Log(www.error);
        }
        else{
            buildingData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData building in buildingData.positions){
                if(!buildingsStarted){
                    GameObject buildingPrefab = buildingsPrefabsVariant[UnityEngine.Random.Range(0, buildingsPrefabsVariant.Length)];
                    buildings[building.id] = Instantiate(buildingPrefab, new Vector3(building.x, building.y, building.z), Quaternion.identity);
                }
            }
            updated = true;
            if(!buildingsStarted){
                buildingsStarted = true;
            }
        }
    }
}
