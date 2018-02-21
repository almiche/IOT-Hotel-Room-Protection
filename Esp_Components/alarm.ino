#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define sensor A0

const char* ssid     = "raffy1968";
const char* password = "raffy2011";
String sensitivity = "";
int start = 0;
const String HOST = "hotelroom-iot-mike.herokuapp.com";


void setup ()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin("raffy1968", "raffy2011");
  pinMode (sensor, INPUT) ;
  initialCalibration();
}

void loop (){
  int currentMotion = analogRead(sensor);
  if(WiFi.status() == WL_CONNECTED) {
    int offset = currentMotion - start;
//    Serial.println("Current: " + currentMotion);
//    Serial.println("Start: " + start );
//    Serial.println("Offset: " + offset);
//    if( offset > sensitivity){
//          getRequest(HOST,"/api/v0.1/alarm/status","location=bedroom");
//        }
//      else{
//         getRequest(HOST,"/api/v0.1/alarm/status","location=nothing");
//      }
  
    }
}

String getRequest(String host,String url,String queryString){
    HTTPClient http;  //Declare an object of class HTTPClient
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      http.begin("http://" + HOST + url + "?" + queryString);  //Specify request destination
      int httpCode = http.GET();                                                                  //Send the request
      String payload;
      if (httpCode > 0) { //Check the returning code
   
        payload = http.getString();   //Get the request response payload
        Serial.println(payload);                     //Print the response payload
      }
   
      http.end();   //Close connection
      return payload;
    }
}

void initialCalibration(){
  Serial.println("Calibrating in 5 seconds ......");
  delay(5000);
  int currentMotion = analogRead(sensor);
  start = currentMotion; 
  Serial.println("Current motion is now : " + start );
  sensitivity = getRequest(HOST,"/api/v1.0/configuration/sensitivity","");
  Serial.println("Sensitivity is now : " + sensitivity );
}
