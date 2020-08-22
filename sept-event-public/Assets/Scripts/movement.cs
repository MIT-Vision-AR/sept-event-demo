using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Reflection;
public class movement : MonoBehaviour
{
    // Start is called before the first frame update
    
    public float speed;
    public float jumpvelocity;
    private int list_post;
    UdpClient client;
    Thread receiveThread;
    private string message;

    void Start()
    {
        list_post = 8300;//this must be same on both sides


        print("Starting connection now");
        InitConnection();

    }
    void InitConnection()
    {
        print("UDP Initialized");

        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

    }
    private void ReceiveData()
    {
        client = new UdpClient(list_post);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), list_post); //connecting
                byte[] data = client.Receive(ref anyIP); //recieving from server

                message = Encoding.UTF8.GetString(data); //UTF-8 form
            }
            catch (Exception e)
            {
                print(e.ToString());
            }
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        // float horizontal = Input.GetAxis("Horizontal");
        //float vertical = Input.GetAxis("Vertical");
        // print(horizontal + " " + vertical);
        //Vector3 move = new Vector3(horizontal, 0.0f, vertical);
        // transform.position += new Vector3(horizontal * speed * Time.deltaTime,0f , vertical * speed * Time.deltaTime);

        if (Input.GetKey(KeyCode.W) || message == "up")

            transform.position += transform.TransformDirection(Vector3.forward * Time.deltaTime * speed);

        if (Input.GetKey(KeyCode.A) || message == "left")

            transform.position += transform.TransformDirection(Vector3.left * Time.deltaTime * speed);
        if (Input.GetKey(KeyCode.S) || message == "down")

            GetComponent<Rigidbody>().velocity = Vector3.zero;

        if (Input.GetKey(KeyCode.D) || message == "right")

            transform.position += transform.TransformDirection(Vector3.right * Time.deltaTime * speed);
        if (Input.GetKey(KeyCode.Space)|| message == "fist")
            GetComponent<Rigidbody>().velocity = Vector3.up * jumpvelocity;

    }
}
