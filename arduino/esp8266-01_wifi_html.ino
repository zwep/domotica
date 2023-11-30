#include <ESP8266WiFi.h>

//https://github.com/asksensors/AskSensors-ESP8266-DHT/blob/master/dht11_https_get.ino

// Wifi settings
const char* ssid = "";
const char* password = "";


//Service Port
WiFiServer server(80);

void setup() {
    //Serial.begin(115200);
    Serial.begin(9600);
    delay(10);

    // Connect to WiFi network
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
    client.println("Hello");
    client.println("</html>");
}