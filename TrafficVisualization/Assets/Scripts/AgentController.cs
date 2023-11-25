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
public class CarData : AgentData{

    public CarData(string id, float x, float y, float z, float speed, float rotation) : base(id, x, y, z){

    }
}

[Serializable]
public class DesinationData : AgentData{
    
    public DesinationData(string id, float x, float y, float z) : base(id, x, y, z){

    }
}