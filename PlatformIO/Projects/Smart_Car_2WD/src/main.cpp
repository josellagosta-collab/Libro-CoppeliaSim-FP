#include <Arduino.h>

const int ENA = 5;
const int ENB = 6;

const int IN1 = 7;
const int IN2 = 8;
const int IN3 = 9;
const int IN4 = 10;

const int VELOCIDAD = 250;
const unsigned long TIEMPO_PRUEBA = 3000;
const unsigned long TIEMPO_PAUSA = 1500;

void parar()
{
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void probarMotorAAdelante()
{
    Serial.println("Motor A adelante: OUT1/OUT2");

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, 0);
}

void probarMotorAAtras()
{
    Serial.println("Motor A atras: OUT1/OUT2");

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, 0);
}

void probarMotorBAdelante()
{
    Serial.println("Motor B adelante: OUT3/OUT4");

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);

    analogWrite(ENA, 0);
    analogWrite(ENB, VELOCIDAD);
}

void probarMotorBAtras()
{
    Serial.println("Motor B atras: OUT3/OUT4");

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    analogWrite(ENA, 0);
    analogWrite(ENB, VELOCIDAD);
}

void probarAmbosMotores()
{
    Serial.println("Ambos motores");

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);

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
    Serial.println("Diagnostico L298N: ENA D5, ENB D6, IN1 D7, IN2 D8, IN3 D9, IN4 D10");
}

void loop()
{
    probarMotorAAdelante();
    delay(TIEMPO_PRUEBA);

    parar();
    delay(TIEMPO_PAUSA);

    probarMotorAAtras();
    delay(TIEMPO_PRUEBA);

    parar();
    delay(TIEMPO_PAUSA);

    probarMotorBAdelante();
    delay(TIEMPO_PRUEBA);

    parar();
    delay(TIEMPO_PAUSA);

    probarMotorBAtras();
    delay(TIEMPO_PRUEBA);

    parar();
    delay(TIEMPO_PAUSA);

    probarAmbosMotores();
    delay(TIEMPO_PRUEBA);

    parar();
    delay(TIEMPO_PAUSA);
}
