#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoJson.h>
#define sensor A0

const char* ssid     = "raffy1968";
const char* password = "raffy2011";
int sensitivity = 0;
int start = 0;
const String HOST = "hotelroom-iot-mike.herokuapp.com";
ESP8266WiFiMulti WiFiMulti;


void setup ()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("raffy1968", "raffy2011");
  pinMode (sensor, INPUT) ;
  initialCalibration();
}

void loop (){
  int currentMotion = analogRead(sensor);
  if((WiFiMulti.run() == WL_CONNECTED)) {
    int offset = currentMotion - start;
    Serial.prinln(currentMotion + " - " + start + " = " + offset);
    //Temporarily in comments for testing purposes
//    if( offset > sensitivity){
//          getRequest(HOST,"/api/v0.1/alarm/status","location=bedroom");
//        }
//      else{
//         getRequest(HOST,"/api/v0.1/alarm/status","location=nothing");
//      }
  
    }
}

String getRequest(String host,String url,String queryString){
    WiFiClient client;
    const int httpPort = 80;
    if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
    String url = url + "?" + queryString;
    Serial.print("Requesting URL: ");
    Serial.println(url);
    
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" + 
                 "Connection: close\r\n\r\n");
    return client.println();
}

void initialCalibration(){
  delay(5000);
  Serial.prinln("Calibrating in 5 seconds ......");
  int currentMotion = analogRead(sensor);
  start = currentMotion; 
  sensitivty = getRequest(HOST,"/api/v1.0/alarm/status","").toInt();
}
