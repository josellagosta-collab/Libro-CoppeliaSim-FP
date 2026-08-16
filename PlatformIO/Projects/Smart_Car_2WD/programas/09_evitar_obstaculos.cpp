#include <Arduino.h>
#include <Servo.h>

const int PIN_SERVO = 3;
const int ENA = 5;
const int ENB = 6;
const int IN1 = 7;
const int IN2 = 8;
const int IN3 = 9;
const int IN4 = 10;
const int TRIG = 11;
const int ECHO = 12;

const int VELOCIDAD = 200;
const int ANGULO_IZQUIERDA = 0;
const int ANGULO_CENTRO = 90;
const int ANGULO_DERECHA = 180;
const float DISTANCIA_OBSTACULO = 20.0;

const unsigned long PAUSA_SERVO = 500;
const unsigned long TIEMPO_GIRO = 550;
const unsigned long TIEMPO_GIRO_BLOQUEADO = 1000;
const unsigned long PAUSA_DECISION = 200;

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

bool caminoLibre(float distancia)
{
    return distancia < 0 || distancia >= DISTANCIA_OBSTACULO;
}

float mirarDistancia(int angulo)
{
    servoDireccion.write(angulo);
    delay(PAUSA_SERVO);

    float distancia = medirDistanciaCm();

    Serial.print("Angulo ");
    Serial.print(angulo);
    Serial.print(": ");

    if (distancia < 0)
    {
        Serial.println("fuera de alcance");
    }
    else
    {
        Serial.print(distancia, 1);
        Serial.println(" cm");
    }

    return distancia;
}

void parar()
{
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void avanzar()
{
    // Sentidos reales medidos: Motor A posicion 2, Motor B posicion 4.
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, VELOCIDAD);
}

void girarIzquierda(unsigned long tiempoGiro)
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, VELOCIDAD);
    delay(tiempoGiro);
    parar();
}

void girarDerecha(unsigned long tiempoGiro)
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);

    analogWrite(ENA, VELOCIDAD);
    analogWrite(ENB, VELOCIDAD);
    delay(tiempoGiro);
    parar();
}

void evitarObstaculo()
{
    parar();
    delay(PAUSA_DECISION);

    float distanciaIzquierda = mirarDistancia(ANGULO_IZQUIERDA);
    float distanciaDerecha = mirarDistancia(ANGULO_DERECHA);

    servoDireccion.write(ANGULO_CENTRO);
    delay(PAUSA_SERVO);

    bool izquierdaLibre = caminoLibre(distanciaIzquierda);
    bool derechaLibre = caminoLibre(distanciaDerecha);

    if (izquierdaLibre && !derechaLibre)
    {
        Serial.println("Giro a la izquierda");
        girarIzquierda(TIEMPO_GIRO);
    }
    else if (derechaLibre && !izquierdaLibre)
    {
        Serial.println("Giro a la derecha");
        girarDerecha(TIEMPO_GIRO);
    }
    else if (izquierdaLibre && derechaLibre)
    {
        if (distanciaIzquierda >= distanciaDerecha)
        {
            Serial.println("Ambos lados libres: izquierda mas despejada");
            girarIzquierda(TIEMPO_GIRO);
        }
        else
        {
            Serial.println("Ambos lados libres: derecha mas despejada");
            girarDerecha(TIEMPO_GIRO);
        }
    }
    else
    {
        Serial.println("Ambos lados bloqueados: giro largo");
        girarDerecha(TIEMPO_GIRO_BLOQUEADO);
    }
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
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    digitalWrite(TRIG, LOW);
    servoDireccion.attach(PIN_SERVO);
    servoDireccion.write(ANGULO_CENTRO);

    parar();
    Serial.println("Programa 09: evita obstaculos");
    delay(1000);
}

void loop()
{
    servoDireccion.write(ANGULO_CENTRO);
    delay(100);

    float distanciaFrontal = medirDistanciaCm();

    if (distanciaFrontal >= 0)
    {
        Serial.print("Frente: ");
        Serial.print(distanciaFrontal, 1);
        Serial.println(" cm");
    }
    else
    {
        Serial.println("Frente: fuera de alcance");
    }

    if (distanciaFrontal >= 0 && distanciaFrontal < DISTANCIA_OBSTACULO)
    {
        Serial.println("Obstaculo detectado");
        evitarObstaculo();
    }
    else
    {
        avanzar();
    }
}
