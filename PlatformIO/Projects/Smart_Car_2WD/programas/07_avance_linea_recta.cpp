#include <Arduino.h>

const int ENA = 5;
const int ENB = 6;

const int IN1 = 7;
const int IN2 = 8;
const int IN3 = 9;
const int IN4 = 10;

const int VELOCIDAD = 250;
const unsigned long TIEMPO_AVANCE = 2500;
const unsigned long TIEMPO_PAUSA = 1000;

void parar()
{
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void avanzarRecto()
{
    // Sentidos reales medidos: Motor A posicion 2, Motor B posicion 4.
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, VELOCIDAD);
}

void setup()
{
    Serial.begin(9600);

    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    parar();
    Serial.println("Programa 07: avance en linea recta");
}

void loop()
{
    avanzarRecto();
    delay(TIEMPO_AVANCE);

    parar();
    delay(TIEMPO_PAUSA);
}
