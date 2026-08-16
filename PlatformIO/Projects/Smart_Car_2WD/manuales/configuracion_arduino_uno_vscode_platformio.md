# Configuración y prueba de un Arduino UNO compatible con VS Code y PlatformIO

## Objetivo

En este documento se recogen los pasos seguidos para preparar **Visual Studio Code** para programar la placa compatible con **Arduino UNO** instalada en el Smart Car 2WD.

Al finalizar, podremos:

- Programar el Arduino desde VS Code.
- Compilar programas con PlatformIO.
- Cargar los programas por USB.
- Comprobar que la comunicación con la placa funciona correctamente.
- Utilizar este entorno para desarrollar posteriormente el software del Smart Car 2WD.

---

## 1. Hardware utilizado

Para esta primera configuración necesitamos:

- PC con Windows.
- Visual Studio Code.
- Placa compatible con Arduino UNO.
- Cable USB.
- Smart Car 2WD.

La placa utilizada en el robot incorpora un conversor USB-Serie **CH340**.

Para esta primera prueba **no es necesario alimentar los motores**. El Arduino puede permanecer conectado únicamente al PC mediante USB.

---

## 2. Instalar PlatformIO IDE en VS Code

Abrimos **Visual Studio Code**.

En la barra lateral izquierda seleccionamos **Extensiones** o utilizamos:

```text
Ctrl + Shift + X
```

Buscamos:

```text
PlatformIO IDE
```

Instalamos la extensión **PlatformIO IDE**.

---

## 3. Instalar PlatformIO Core

La primera vez que abrimos PlatformIO puede aparecer una pantalla con el mensaje:

```text
Get started with PlatformIO IDE
```

y el botón:

```text
Install PlatformIO Core
```

Pulsamos **Install PlatformIO Core**.

PlatformIO Core es el componente encargado de realizar tareas como:

- Compilar los programas.
- Gestionar las plataformas de desarrollo.
- Gestionar librerías.
- Detectar dispositivos.
- Cargar los programas en el Arduino.

Esperamos a que termine la instalación.

Si VS Code solicita reiniciarse o recargar la ventana, lo hacemos.

---

## 4. Abrir PlatformIO Home

Una vez instalado PlatformIO, podemos acceder a él desde el icono de PlatformIO situado en la barra lateral izquierda.

También podemos utilizar:

```text
Ctrl + Shift + P
```

y buscar:

```text
PlatformIO: Home
```

Se abrirá la pantalla:

```text
PIO Home
```

En ella encontramos opciones como:

```text
New Project
Import Arduino Project
Open Project
Project Examples
```

---

## 5. Crear el proyecto del Smart Car

Pulsamos:

```text
New Project
```

En el asistente **Project Wizard** configuramos:

```text
Name:       Smart_Car_2WD
Board:      Arduino Uno
Framework:  Arduino
```

En **Board** buscamos y seleccionamos:

```text
Arduino Uno
```

En **Framework** seleccionamos:

```text
Arduino
```

Podemos dejar la ubicación predeterminada o seleccionar nuestra carpeta de proyectos.

Finalmente pulsamos:

```text
Finish
```

PlatformIO crea automáticamente la estructura del proyecto.

---

## 6. Estructura del proyecto

El proyecto tendrá aproximadamente esta estructura:

```text
Smart_Car_2WD
│
├── .pio
├── .vscode
├── include
├── lib
├── src
├── test
├── .gitignore
└── platformio.ini
```

Las dos partes que utilizaremos inicialmente son:

```text
platformio.ini
src/main.cpp
```

### `platformio.ini`

Contiene la configuración de la placa y del proyecto.

### `src/main.cpp`

Contiene nuestro programa Arduino.

---

## 7. Comprobar `platformio.ini`

PlatformIO creó automáticamente el archivo con esta configuración:

```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino
```

Esto indica:

- `platform = atmelavr`: utilizamos la plataforma AVR.
- `board = uno`: la placa seleccionada es Arduino UNO.
- `framework = arduino`: utilizamos el framework Arduino.

Por tanto, PlatformIO está correctamente configurado para nuestra placa.

---

## 8. Conectar el Arduino al ordenador

Conectamos el Arduino UNO compatible mediante USB:

```text
PC ───────── USB ───────── Arduino UNO
```

Para esta prueba mantenemos apagada la alimentación de los motores.

El Arduino se alimentará desde el propio puerto USB.

---

## 9. Comprobar el puerto COM en Windows

Abrimos:

```text
Administrador de dispositivos
```

Desplegamos:

```text
Puertos (COM y LPT)
```

En nuestro caso Windows detectó:

```text
USB-SERIAL CH340 (COM9)
```

Por tanto, el Arduino está conectado al:

```text
COM9
```

El nombre **CH340** corresponde al conversor USB-Serie utilizado por muchas placas compatibles con Arduino UNO.

---

## 10. Configurar COM9 en PlatformIO

Como sabemos que nuestra placa utiliza COM9, podemos indicarlo en `platformio.ini`.

El archivo queda:

```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino

upload_port = COM9
monitor_port = COM9
monitor_speed = 9600
```

Las nuevas opciones significan:

### `upload_port`

```ini
upload_port = COM9
```

Indica el puerto utilizado para cargar el programa en Arduino.

### `monitor_port`

```ini
monitor_port = COM9
```

Indica el puerto utilizado por el monitor serie.

### `monitor_speed`

```ini
monitor_speed = 9600
```

Establece la velocidad de comunicación del monitor serie en **9600 baudios**.

> Si Windows asigna otro puerto COM en el futuro, habrá que cambiar `COM9` por el nuevo puerto.

---

## 11. Primera prueba: Blink

Antes de controlar motores, servo o sensores, comprobamos que podemos programar correctamente el Arduino.

Abrimos:

```text
src/main.cpp
```

Introducimos:

```cpp
#include <Arduino.h>

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);

    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
```

Guardamos:

```text
Ctrl + S
```

---

## 12. ¿Qué hace el programa?

La instrucción:

```cpp
pinMode(LED_BUILTIN, OUTPUT);
```

configura el LED integrado del Arduino como salida.

Después:

```cpp
digitalWrite(LED_BUILTIN, HIGH);
```

enciende el LED.

Esperamos:

```cpp
delay(500);
```

es decir, **500 ms = 0,5 segundos**.

Después:

```cpp
digitalWrite(LED_BUILTIN, LOW);
```

apaga el LED durante otros 0,5 segundos.

Como `loop()` se repite continuamente, obtenemos:

```text
LED encendido → 0,5 s
LED apagado   → 0,5 s
LED encendido → 0,5 s
LED apagado   → 0,5 s
...
```

---

## 13. Compilar el programa

Antes de cargarlo debemos comprobar que no contiene errores.

En PlatformIO utilizamos **Build**, identificado normalmente por el símbolo:

```text
✓
```

También podemos utilizar:

```text
Ctrl + Alt + B
```

PlatformIO compilará el proyecto.

Si todo es correcto, al final de la terminal aparecerá:

```text
SUCCESS
```

Esto significa que el código se ha compilado correctamente.

---

## 14. Cargar el programa en Arduino

Con el Arduino conectado mediante USB, utilizamos la opción **Upload** de PlatformIO, normalmente identificada por una flecha:

```text
→
```

PlatformIO utilizará:

```text
COM9
```

para transferir el programa.

Durante este proceso pueden aparecer mensajes relacionados con:

```text
avrdude
```

Esta herramienta se encarga de transferir el programa compilado al microcontrolador del Arduino UNO.

Si la carga termina correctamente veremos:

```text
SUCCESS
```

---

## 15. Comprobar el resultado

Después de cargar el programa observamos el Arduino.

El LED integrado debe:

```text
encenderse
    ↓
esperar 0,5 segundos
    ↓
apagarse
    ↓
esperar 0,5 segundos
    ↓
repetir
```

Si esto ocurre, hemos demostrado que funciona toda la cadena:

```text
VS Code
   │
   ▼
PlatformIO IDE
   │
   ▼
PlatformIO Core
   │
   ▼
Compilador AVR
   │
   ▼
COM9
   │
   ▼
CH340
   │
   ▼
Arduino UNO compatible
   │
   ▼
ATmega328P
```

Por tanto, nuestro Arduino ya puede programarse correctamente desde **Visual Studio Code**.

---

## 16. Prueba opcional del monitor serie

También podemos comprobar la comunicación entre Arduino y VS Code mediante el puerto serie.

Sustituimos temporalmente `main.cpp` por:

```cpp
#include <Arduino.h>

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    Serial.println("Smart Car 2WD funcionando");
    delay(1000);
}
```

Compilamos y cargamos el programa.

Después abrimos el **Serial Monitor** de PlatformIO.

Deberíamos recibir:

```text
Smart Car 2WD funcionando
Smart Car 2WD funcionando
Smart Car 2WD funcionando
...
```

La velocidad debe coincidir con:

```ini
monitor_speed = 9600
```

y con:

```cpp
Serial.begin(9600);
```

---

## 17. Configuración final utilizada

Nuestro `platformio.ini` queda:

```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino

upload_port = COM9
monitor_port = COM9
monitor_speed = 9600
```

Y el proyecto:

```text
Smart_Car_2WD
│
├── .pio
├── .vscode
├── include
├── lib
├── src
│   └── main.cpp
├── test
├── .gitignore
└── platformio.ini
```

---

## 18. Próximos pasos para el Smart Car 2WD

Una vez comprobado el entorno de programación, podemos avanzar progresivamente:

1. Probar el motor izquierdo.
2. Probar el motor derecho.
3. Controlar ambos motores mediante el L298N.
4. Programar avance y retroceso.
5. Programar giros.
6. Añadir control PWM de velocidad.
7. Probar el servo.
8. Probar el HC-SR04.
9. Combinar servo y sensor ultrasónico.
10. Crear un programa autónomo para evitar obstáculos.
11. Añadir sensores seguidores de línea.
12. Comunicar el Arduino con Python.
13. Incorporar posteriormente visión artificial con OpenCV.

---

# Resultado

El entorno queda preparado para desarrollar el Smart Car 2WD utilizando:

```text
Visual Studio Code
        +
PlatformIO
        +
Arduino Framework
        +
Arduino UNO compatible
```

La prueba **Blink** permite verificar de forma sencilla que el código se compila y se transfiere correctamente desde VS Code hasta el Arduino antes de comenzar a trabajar con los motores y sensores del robot.
