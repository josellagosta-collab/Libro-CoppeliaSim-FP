#include <Arduino.h>

const int TRIG = 11;
const int ECHO = 12;

void setup()
{
    Serial.begin(9600);

    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    digitalWrite(TRIG, LOW);

    Serial.println("Prueba HC-SR04 en TRIG D11 / ECHO D12");
}

void loop()
{
    // Aseguramos que TRIG empieza a nivel bajo
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);

    // Pulso de disparo de 10 microsegundos
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    // Medimos cuánto tiempo permanece ECHO en HIGH
    unsigned long tiempo = pulseIn(ECHO, HIGH, 30000);

    if (tiempo == 0)
    {
        Serial.println("No se detecta objeto / fuera de alcance");
    }
    else
    {
        // Conversión del tiempo en distancia
        float distancia = tiempo * 0.0343 / 2.0;

        Serial.print("Distancia: ");
        Serial.print(distancia, 1);
        Serial.println(" cm");
    }

    delay(250);
}
