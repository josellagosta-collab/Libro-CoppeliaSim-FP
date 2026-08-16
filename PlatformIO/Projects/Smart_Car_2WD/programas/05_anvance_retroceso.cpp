#include <Arduino.h>

const int ENA = 5;
const int ENB = 6;

const int IN1 = 7;
const int IN2 = 8;
const int IN3 = 9;
const int IN4 = 10;

const int VELOCIDAD_IZQUIERDA = 255;
const int VELOCIDAD_DERECHA = 255;
const unsigned long TIEMPO_MOVIMIENTO = 10000;

void avanzar()
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);

    analogWrite(ENA, VELOCIDAD_IZQUIERDA);
    analogWrite(ENB, VELOCIDAD_DERECHA);
}

void retroceder()
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);

    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    analogWrite(ENA, VELOCIDAD_IZQUIERDA);
    analogWrite(ENB, VELOCIDAD_DERECHA);
}

void setup()
{
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
}

void loop()
{
    avanzar();
    delay(TIEMPO_MOVIMIENTO);

    retroceder();
    delay(TIEMPO_MOVIMIENTO);
}
