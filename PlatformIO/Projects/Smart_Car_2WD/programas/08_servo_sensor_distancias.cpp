#include <Arduino.h>
#include <Servo.h>

const int PIN_SERVO = 3;
const int TRIG = 11;
const int ECHO = 12;

const int ANGULO_IZQUIERDA = 0;
const int ANGULO_CENTRO = 90;
const int ANGULO_DERECHA = 180;
const int PASO_BARRIDO = 5;
const int PAUSA_SERVO = 250;

Servo servoDireccion;

float medirDistanciaCm()
{
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    unsigned long tiempo = pulseIn(ECHO, HIGH, 30000);

    if (tiempo == 0)
    {
        return -1.0;
    }

    return tiempo * 0.0343 / 2.0;
}

void mostrarDistancia(int angulo)
{
    float distancia = medirDistanciaCm();

    Serial.print("Angulo: ");
    Serial.print(angulo);
    Serial.print(" grados | Distancia: ");

    if (distancia < 0)
    {
        Serial.println("fuera de alcance");
    }
    else
    {
        Serial.print(distancia, 1);
        Serial.println(" cm");
    }
}

void moverYMedir(int desde, int hasta, int paso)
{
    for (int angulo = desde; paso > 0 ? angulo <= hasta : angulo >= hasta; angulo += paso)
    {
        servoDireccion.write(angulo);
        delay(PAUSA_SERVO);
        mostrarDistancia(angulo);
    }
}

void setup()
{
    Serial.begin(9600);

    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    digitalWrite(TRIG, LOW);

    servoDireccion.attach(PIN_SERVO);
    servoDireccion.write(ANGULO_CENTRO);

    Serial.println("Programa 08: servo + HC-SR04");
    Serial.println("Servo D3, TRIG D11, ECHO D12");
    delay(1000);
}

void loop()
{
    moverYMedir(ANGULO_CENTRO, ANGULO_DERECHA, PASO_BARRIDO);
    delay(500);

    moverYMedir(ANGULO_DERECHA, ANGULO_IZQUIERDA, -PASO_BARRIDO);
    delay(500);

    moverYMedir(ANGULO_IZQUIERDA, ANGULO_CENTRO, PASO_BARRIDO);
    delay(500);
}
