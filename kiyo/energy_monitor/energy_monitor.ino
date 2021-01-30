#include "secrets.h"
#include "EmonLib.h"
#include "WiFi.h"
#include "HTTPClient.h"

EnergyMonitor emon1;
 
const char* ssid = SID2;
const char* password = PWD2; 
 
void setup() {
 
  Serial.begin(9600);
  emon1.current(26, 111.1); 
  delay(4000);   //Delay needed before calling the WiFi.begin
 
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
}
 
void loop() {

 double Irms = emon1.calcIrms(1480); 
 
 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
 
   HTTPClient http; 

   String url = URL;
   url += Irms;
 
   http.begin(url);  //Specify destination for HTTP request
   http.addHeader("Content-Type", "application/json");             //Specify content-type header
 
   int httpResponseCode = http.PUT("POSTING from ESP32");   //Send the actual POST request
 
   if(httpResponseCode>0){
 
    String response = http.getString();                       //Get the response to the request

    Serial.println(Irms); 
    Serial.println(httpResponseCode);   //Print return code
    Serial.println(response);           //Print request answer
 
   }else{
 
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
 
   }
 
   http.end();  //Free resources
 
 }else{
 
    Serial.println("Error in WiFi connection");   
 
 }
 
  delay(1000);  //Send a request every 10 seconds
 
}
