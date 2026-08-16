#include <Arduino.h>
#include <Servo.h>

const int PIN_SERVO = 3;

const int ANGULO_CENTRO = 90;
const int GIRO_A_CADA_LADO = 45;
const int ANGULO_DERECHA = ANGULO_CENTRO + GIRO_A_CADA_LADO;
const int ANGULO_IZQUIERDA = ANGULO_CENTRO - GIRO_A_CADA_LADO;
const int PAUSA_POSICION = 1500;

Servo servoDireccion;

void setup()
{
    Serial.begin(9600);
    Serial.println("Prueba servo en D3");
    Serial.print("Angulo centro/frente: ");
    Serial.println(ANGULO_CENTRO);

    servoDireccion.attach(PIN_SERVO);
    servoDireccion.write(ANGULO_CENTRO);
    delay(2000);
}

void loop()
{
    Serial.println("Centro");
    servoDireccion.write(ANGULO_CENTRO);
    delay(PAUSA_POSICION);

    Serial.println("Girando a la derecha");
    servoDireccion.write(ANGULO_DERECHA);
    delay(PAUSA_POSICION);

    Serial.println("Girando a la izquierda");
    servoDireccion.write(ANGULO_IZQUIERDA);
    delay(PAUSA_POSICION);

    Serial.println("Volviendo al frente");
    servoDireccion.write(ANGULO_CENTRO);
    delay(PAUSA_POSICION);
}
