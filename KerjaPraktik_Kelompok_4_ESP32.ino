//inisialisasi library yang digunakan
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <ThingSpeak.h>

//setting code untuk menyambungkan ESP32 ke WIFI
WiFiClient  client;
const char* ssid = "ssid";
const char* password = "password";
unsigned long myChannelNumber = 1458775;
const char * myWriteAPIKey = "75OS105VHUXSEDFY";
unsigned long lastTime = 0;
unsigned long timerDelay = 30000;

//inisialisasi variabel 
const int oneWireBus = 33;
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);
float temperatureC;
const int ph_pin1 = 32;
float nilai_analogPH;
double TeganganPH;
float PH7 = 0.049;
float PH4 = 0.812;
float PH;
const int ph_pin2 = 35;
float nilai_analogTurbidity;
float TeganganTurbidity;
float Turbidity;


void setup() { 
  Serial.begin(9600);
  sensors.begin();
  pinMode (ph_pin1, INPUT);
  pinMode (ph_pin2, INPUT);
  WiFi.mode(WIFI_STA);    
  ThingSpeak.begin(client);
}


void loop (){
  if ((millis() - lastTime) > timerDelay) {
    
    if(WiFi.status() != WL_CONNECTED){
      Serial.print("Attempting to connect");
      while(WiFi.status() != WL_CONNECTED){
        WiFi.begin(ssid, password); 
        delay(5000);     
      } 
      Serial.println("\nConnected.");
    }
      
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  nilai_analogPH = analogRead (ph_pin1);
  TeganganPH = (3.3/4095)*nilai_analogPH;
  PH = 7.00 + ((PH7 - TeganganPH)/((PH4-PH7)/3));
  nilai_analogTurbidity = analogRead (ph_pin2);
  TeganganTurbidity = (3.3/4095)* nilai_analogTurbidity;
  Turbidity = (-331.3*(TeganganTurbidity)) + 1089;
  Serial.print("Temperature : ");
  Serial.print(temperatureC);
  Serial.println(" ºC ");
  Serial.print("PH: ");
  Serial.println(PH, 2);
  Serial.print("Turbidity : ");
  Serial.print(Turbidity, 2);
  Serial.println(" NTU ");
  
  ThingSpeak.setField(1, temperatureC);
  ThingSpeak.setField(2, PH);
  ThingSpeak.setField(3, Turbidity);
  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  if(x == 200){
      Serial.println("Channel update successful.");
  }
  else{
      Serial.println("Problem updating channel. HTTP error code " + String(x));
  }
  lastTime = millis();
  }
  delay(15000);
}
