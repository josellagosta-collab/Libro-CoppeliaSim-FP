# Manual de montaje del Smart Car 2WD

## 1. Componentes utilizados

Este manual corresponde al montaje del robot **Smart Car 2WD** con los componentes que se han identificado durante el montaje:

- Chasis Smart Car 2WD.
- 2 motores reductores DC.
- 2 ruedas motrices.
- 1 rueda loca.
- Portapilas **UM-4×3** para 4 pilas AA.
- Interruptor.
- Tornillos, tuercas, separadores y soportes.
- Placa compatible con **Arduino UNO**.
- **Sensor Shield V5.0**.
- Controlador de motores **L298N**.
- Microservo.
- Sensor ultrasónico **HC-SR04**.
- Cables Dupont.

### Herramientas recomendadas

- Destornillador de estrella pequeño.
- Alicates pequeños.

---

## 2. Preparación del chasis

1. Retira las películas protectoras del chasis acrílico si todavía las lleva.
2. Identifica la parte superior e inferior del chasis.
3. Comprueba que los agujeros y ranuras están libres.

En este montaje consideraremos como **parte delantera** el extremo donde se instalarán la rueda loca y el sensor ultrasónico.

---

## 3. Montaje de los motores

1. Coloca los soportes de plástico de los motores en las ranuras correspondientes.
2. Introduce un motor en cada lateral.
3. Los ejes de los motores deben quedar orientados hacia el exterior.
4. Coloca los tornillos de fijación.
5. Aprieta las tuercas sin deformar los soportes.
6. Comprueba que ambos motores están correctamente alineados.

Los terminales o cables de los motores deben quedar accesibles para conectarlos posteriormente al L298N.

---

## 4. Montaje de las ruedas

1. Alinea cada rueda con el eje de su motor.
2. Presiona suavemente hasta que quede correctamente introducida.
3. No golpees las ruedas para introducirlas.
4. Comprueba que ambas pueden girar sin rozar el chasis.

---

## 5. Montaje de la rueda loca

1. Coloca la rueda loca en la parte delantera inferior del chasis.
2. Haz coincidir sus agujeros con los del chasis.
3. Introduce los tornillos.
4. Coloca y aprieta las tuercas.
5. Comprueba que la rueda puede girar libremente en todas las direcciones.

---

## 6. Montaje del portapilas

El portapilas marcado como **UM-4×3** utiliza **4 pilas AA**.

Con pilas alcalinas:

```text
4 × 1,5 V = 6 V
```

Para instalarlo:

1. Coloca el portapilas sobre la parte superior del chasis.
2. Alinea sus agujeros con los del chasis.
3. Sujétalo utilizando los tornillos o separadores correspondientes.
4. Deja accesibles los cables rojo y negro.

> No introduzcas las pilas hasta haber terminado y revisado el cableado.

---

## 7. Montaje del interruptor

1. Localiza el hueco rectangular previsto para el interruptor.
2. Introduce el interruptor hasta que quede firmemente sujeto.
3. Comprueba que puede accionarse sin dificultad.

El interruptor puede instalarse en serie con el positivo de la alimentación para encender y apagar el robot.

---

## 8. Montaje del Arduino UNO

La placa utilizada es compatible con **Arduino UNO**.

1. Coloca separadores entre el chasis y el Arduino.
2. Sitúa el Arduino de forma que el puerto USB quede accesible.
3. Atorníllalo sin apretar excesivamente.
4. Comprueba que la parte inferior de la placa no toca directamente ninguna pieza metálica.

---

## 9. Instalación del Sensor Shield V5.0

1. Alinea el **Sensor Shield V5.0** con los conectores del Arduino UNO.
2. Comprueba cuidadosamente que todos los pines coinciden.
3. Introduce el shield verticalmente y de forma uniforme.

Los conectores del shield están normalmente identificados como:

- **G** → GND.
- **V** → alimentación.
- **S** → señal.

> Comprueba siempre las letras impresas en la placa antes de conectar un dispositivo.

---

## 10. Montaje del controlador L298N

El **L298N** controla los dos motores DC.

Fíjalo al chasis mediante tornillos o separadores y deja accesibles sus conexiones.

### Conexión de los motores

```text
Motor izquierdo → OUT1 y OUT2
Motor derecho   → OUT3 y OUT4
```

Si posteriormente uno de los motores gira en sentido contrario al esperado, pueden intercambiarse sus dos cables.

---

## 11. Conexión del L298N al Arduino

Para las primeras pruebas pueden dejarse colocados los jumpers **ENA** y **ENB** del L298N.

Utilizaremos:

| Arduino | L298N | Función |
|---|---|---|
| D7 | IN1 | Dirección motor A |
| D8 | IN2 | Dirección motor A |
| D9 | IN3 | Dirección motor B |
| D10 | IN4 | Dirección motor B |
| GND | GND | Masa común |

La conexión de **GND entre Arduino y L298N es imprescindible**.

---

## 12. Control de velocidad

Cuando queramos controlar la velocidad independientemente:

1. Retira el jumper **ENA**.
2. Retira el jumper **ENB**.
3. Conecta:

| Arduino | L298N |
|---|---|
| D5 (PWM) | ENA |
| D6 (PWM) | ENB |

Arduino podrá entonces regular la velocidad mediante PWM.

---

## 13. Montaje y conexión del servo

El microservo tiene normalmente tres cables:

| Cable | Función |
|---|---|
| Marrón/negro | GND |
| Rojo | +5 V |
| Naranja/amarillo | Señal |

Utilizaremos el pin **D3**.

En el Sensor Shield:

```text
Servo GND    → G de D3
Servo +5 V   → V de D3
Servo señal  → S de D3
```

El servo servirá para orientar el sensor ultrasónico hacia diferentes direcciones.

---

## 14. Montaje del HC-SR04

El sensor ultrasónico **HC-SR04** dispone de:

- VCC
- TRIG
- ECHO
- GND

Lo conectaremos de la siguiente manera:

| HC-SR04 | Arduino / Sensor Shield |
|---|---|
| VCC | 5 V / V |
| TRIG | S de D11 |
| ECHO | S de D12 |
| GND | G / GND |

Monta el HC-SR04 sobre el soporte unido al servo.

De esta forma, Arduino podrá girar el sensor para medir distancias hacia la izquierda, centro y derecha.

---

## 15. Resumen de pines

| Pin Arduino | Dispositivo |
|---|---|
| D3 | Servo |
| D5 | ENA L298N (PWM) |
| D6 | ENB L298N (PWM) |
| D7 | IN1 L298N |
| D8 | IN2 L298N |
| D9 | IN3 L298N |
| D10 | IN4 L298N |
| D11 | TRIG HC-SR04 |
| D12 | ECHO HC-SR04 |

---

## 16. Alimentación

Los motores pueden producir picos de corriente y ruido eléctrico. Para las primeras pruebas es conveniente:

- Alimentar el Arduino mediante **USB**.
- Alimentar los motores a través del **L298N** con una fuente adecuada.
- Mantener una **masa común (GND)** entre Arduino y L298N.

Esquema conceptual:

```text
                Alimentación motores
                         │
                         ▼
                       L298N
                    ┌────┴────┐
                    ▼         ▼
                 Motor I    Motor D
                    ▲
                    │ señales
                    │
              Arduino UNO
                │       │
                ▼       ▼
              Servo   HC-SR04

Arduino GND ───────── L298N GND
```

> No conectes una alimentación a la placa sin comprobar previamente la tensión y la polaridad.

---

## 17. Comprobación antes de encender

Antes de alimentar el robot comprueba:

- [ ] Los motores están firmemente sujetos.
- [ ] Las ruedas giran libremente.
- [ ] La rueda loca gira correctamente.
- [ ] Arduino está correctamente fijado.
- [ ] El Sensor Shield está correctamente insertado.
- [ ] El L298N está sujeto al chasis.
- [ ] Ningún cable puede tocar las ruedas.
- [ ] No existen cables pelados que puedan provocar cortocircuitos.
- [ ] La polaridad de alimentación es correcta.
- [ ] Arduino y L298N comparten GND.
- [ ] El servo está conectado respetando G, V y S.
- [ ] El HC-SR04 está conectado correctamente.

---

## 18. Orden recomendado de pruebas

No pruebes todo simultáneamente la primera vez.

Realiza las pruebas en este orden:

1. Arduino conectado por USB.
2. Servo.
3. HC-SR04.
4. Motor izquierdo.
5. Motor derecho.
6. Ambos motores.
7. Avance y retroceso.
8. Giros.
9. Control PWM de velocidad.
10. Servo + HC-SR04.
11. Integración completa.

> Durante las primeras pruebas de los motores, mantén el robot levantado para que las ruedas puedan girar libremente.

---

## 19. Funcionamiento autónomo previsto

Una vez montado y programado, podemos hacer que el robot funcione de esta manera:

1. El HC-SR04 mide la distancia frontal.
2. Si no hay obstáculos, el robot avanza.
3. Si detecta un obstáculo, se detiene.
4. El servo gira el HC-SR04 hacia la izquierda.
5. Arduino mide la distancia izquierda.
6. El servo gira hacia la derecha.
7. Arduino mide la distancia derecha.
8. Compara ambas distancias.
9. Gira el robot hacia el lado que tenga mayor espacio.
10. Vuelve a avanzar.

---

## 20. Programación

La placa de control está basada en **Arduino UNO**, por lo que se programa normalmente en **C/C++ para Arduino**.

Puede programarse desde:

- Arduino IDE.
- VS Code con PlatformIO.

Posteriormente también puede comunicarse mediante puerto serie con un programa Python ejecutado en un ordenador o Raspberry Pi, permitiendo añadir funciones como **OpenCV y visión artificial**.

---

## Esquema general del Smart Car 2WD

```text
                    HC-SR04
                  👁       👁
                       │
                     SERVO
                       │ D3
                       ▼
              ┌─────────────────┐
              │   ARDUINO UNO   │
              │ + Sensor Shield │
              └────────┬────────┘
                       │
          D7-D10       │       D5-D6 PWM
                       ▼
                  ┌─────────┐
                  │  L298N  │
                  └──┬───┬──┘
                     │   │
              ┌──────┘   └──────┐
              ▼                 ▼
        MOTOR IZQUIERDO    MOTOR DERECHO
              │                 │
              O                 O
```

**Smart Car 2WD — Manual de montaje y conexiones**
