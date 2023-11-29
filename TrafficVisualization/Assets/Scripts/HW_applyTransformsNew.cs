using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HW_applyTransformsNew : MonoBehaviour
{
    [SerializeField] Vector3 displacement;

    // [SerializeField] float angle;
    // [SerializeField] AXIS rotationAxis;
    [SerializeField] GameObject WheelOriginal;

    [SerializeField] Vector3 wheelScale;

    [SerializeField] Vector3[] wheelPositions = new Vector3[4];

    private GameObject[] wheels;


    Mesh mesh;
    Mesh[] wheelsMesh = new Mesh[4];
    Vector3[] baseVertices; //vertices originakes
    Vector3[][] wheelsBaseVertices = new Vector3[4][];

    Vector3[] newVertices; //vertices nuevos
    Vector3[][] wheelsNewVertices = new Vector3[4][]; //vertices nuevos

    // Start is called before the first frame update
    void Start()
    {
        // Vector3 wheelScale = new Vector3(0.39f, 0.39f, 0.39f);

        wheels = new GameObject[4];
        for (int i = 0; i < 4; i++)
        {
            Matrix4x4 scale = HW_Transforms.ScaleMat(wheelScale.x, wheelScale.y, wheelScale.z);

            wheels[i] = Instantiate(WheelOriginal);

            wheelsMesh[i] = wheels[i].GetComponentInChildren<MeshFilter>().mesh;

            wheelsBaseVertices[i] = wheelsMesh[i].vertices;

            wheelsNewVertices[i] = new Vector3[wheelsBaseVertices[i].Length];


            for (int j = 0; j < wheelsBaseVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelsBaseVertices[i][j].x, wheelsBaseVertices[i][j].y, wheelsBaseVertices[i][j].z, 1);
                wheelsNewVertices[i][j] = scale * temp;
                wheelsBaseVertices[i][j] = wheelsNewVertices[i][j];

            }

        }


        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;

        //Allocate memory for the copy of the vertex list
        newVertices = new Vector3[baseVertices.Length];

        //Copy the coordinates
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }


    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // Vector3[] wheelPositions = new Vector3[4]{
        //     new Vector3(0.85f,0.345f,1.535f),
        //     new Vector3(-0.85f,0.345f,1.535f),
        //     new Vector3(-0.85f,0.345f,-1.535f),
        //     new Vector3(0.85f,0.345f,-1.535f)
        // };

        float angleRad = Mathf.Atan2(displacement.z, displacement.x);
        float anglePos = angleRad * Mathf.Rad2Deg;
        float angle = 360 - anglePos;

        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle , AXIS.Y); //cuadritos x segundo time=tiempo acumulado
        Matrix4x4 composite = rotate;

        Matrix4x4 rotateWheel = HW_Transforms.RotateMat(-379 * Time.time, AXIS.X);

        for (int i = 0; i < baseVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp;

        }

        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();


        for (int i = 0; i < 4; i++)
        {
            // Matrix4x4 scale = HW_Transforms.ScaleMat(wheelScale.x,wheelScale.y, wheelScale.z);
            
            Matrix4x4 moveWheels = HW_Transforms.TranslationMat(wheelPositions[i].x, wheelPositions[i].y, wheelPositions[i].z);
            Matrix4x4 wheelsTransform = composite * moveWheels * rotateWheel;

            for (int j = 0; j < wheelsBaseVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelsBaseVertices[i][j].x, wheelsBaseVertices[i][j].y, wheelsBaseVertices[i][j].z, 1);
                wheelsNewVertices[i][j] = wheelsTransform * temp;
            }

            

            wheelsMesh[i].vertices = wheelsNewVertices[i];
            wheelsMesh[i].RecalculateNormals();
            wheelsMesh[i].RecalculateBounds();
        }



    }

}
