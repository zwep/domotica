#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <Adafruit_Sensor.h>
#include <DHT_U.h>
#include <DHT.h>

//https://github.com/asksensors/AskSensors-ESP8266-DHT/blob/master/dht11_https_get.ino
// Tried
// 3.1.2 : 0 networks
// 2.4.2 : 0 networks
// 2.4.0: 0 networks
// 2.3.0: 0 networks
// Wifi settings
const char* ssid = "";
const char* password = "";


// Set DHT properties
#define DHTPIN 2
#define DHTTYPE DHT22
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;
float myTemperature = 0, myHumidity = 0;

//Service Port
WiFiServer server(80);

void setup() {
    Serial.begin(9600);
    delay(10);

    // Connect to WiFi network
    int numberOfNetworks = WiFi.scanNetworks();
    Serial.println();
    Serial.println();
    Serial.print("Number of networks: ");
    Serial.println(numberOfNetworks);
    for(int i =0; i<numberOfNetworks; i++){
      Serial.print("Network name: ");
      Serial.println(WiFi.SSID(i));
      Serial.print("Signal strength: ");
      Serial.println(WiFi.RSSI(i));
      Serial.println("-----------------------");

    }
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    // Start the server
    server.begin();
    Serial.println("Server started");

    // Print the IP address
    Serial.print("Use this URL to connect: ");
    Serial.print("http://");
    Serial.print(WiFi.localIP());
    Serial.println("/");

    // Checking out content of DHT22
    // Initialize device.
    dht.begin();
    Serial.println("DHT22 Unified Sensor Example");
    // Print temperature sensor details.
    sensor_t sensor;
    dht.temperature().getSensor(&sensor);
    Serial.println("------------------------------------");
    Serial.println("Temperature");
    Serial.print  ("Sensor:       "); Serial.println(sensor.name);
    Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
    Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
    Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" *C");
    Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" *C");
    Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" *C");
    Serial.println("------------------------------------");
    // Print humidity sensor details.
    dht.humidity().getSensor(&sensor);
    Serial.println("------------------------------------");
    Serial.println("Humidity");
    Serial.print  ("Sensor:       "); Serial.println(sensor.name);
    Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
    Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
    Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println("%");
    Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println("%");
    Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println("%");
    Serial.println("------------------------------------");
    // Set delay between sensor readings based on sensor details.
    delayMS = sensor.min_delay / 1000;
}

void loop() {
    // Delay between measurements.
    delay(delayMS);

    // Check if a client has connected
    WiFiClient client = server.available();
    if (!client) {
        return;
    }

    // Return the output of the read pin
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println(""); //  do not forget this one
    client.println("<!DOCTYPE HTML>");
    client.println("<html>");
    // Read data from DHT
    // Get temperature event and print its value.
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    if (isnan(event.temperature)) {
        client.println("Error reading temperature!");
    }
    else {
        // Update temperature and humidity
        myTemperature = (float)event.temperature;
        client.println("Temperature: ");
        client.println(myTemperature);
        client.println(" C");
//         Serial.print("Temperature: ");
//         Serial.print(myTemperature);
//         Serial.println(" C");
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&event);
    if (isnan(event.relative_humidity)) {
        client.println("Error reading humidity!");
    }
    else {
        myHumidity = (float)event.relative_humidity;
        client.println("Humidity: ");
        client.println(myHumidity);
        client.println("%");
//         Serial.print("Humidity: ");
//         Serial.print(myHumidity);
//         Serial.println("%");
    }
    client.println("</html>");
}