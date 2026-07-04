::: chapter-cover
number: 24
title: Comunicación industrial
time: 6 horas
level: ⭐⭐⭐⭐☆ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender la importancia de las comunicaciones industriales en la automatización moderna.
- Identificar los principales protocolos utilizados en la Industria 4.0.
- Diferenciar las características de OPC UA, MQTT, TCP/IP y REST API.
- Comprender cómo intercambiar información entre CoppeliaSim y un PLC.
- Preparar el entorno para desarrollar aplicaciones industriales conectadas.
:::

# Capítulo 24 · Comunicación industrial

## ¿Por qué necesita comunicarse un robot?

Hasta este momento hemos trabajado con robots capaces de desplazarse, manipular objetos y comunicarse con aplicaciones desarrolladas en Python o mediante ROS 2.

Sin embargo, en una fábrica moderna un robot rara vez trabaja de forma aislada.

Lo habitual es que forme parte de un sistema mucho más amplio donde diferentes dispositivos intercambian información continuamente.

Por ejemplo, un robot industrial puede:

- recibir órdenes desde un PLC;
- enviar el estado de una operación a un sistema SCADA;
- consultar una base de datos para obtener información sobre una pieza;
- publicar datos de producción en un servidor MQTT;
- intercambiar información con un sistema MES o ERP.

Todos estos dispositivos necesitan utilizar un lenguaje común para poder comunicarse.

Ese lenguaje viene definido por los **protocolos de comunicación industrial**.

Durante este capítulo aprenderemos los más utilizados en la actualidad y veremos cómo integrarlos con CoppeliaSim.

Aunque utilizaremos el simulador como plataforma de aprendizaje, los conceptos estudiados son exactamente los mismos que encontraremos posteriormente en una instalación industrial real.

::: teacher
content:

Es importante transmitir al alumnado que los protocolos de comunicación no son exclusivos de CoppeliaSim.

El simulador simplemente reproduce el comportamiento de los sistemas industriales reales, permitiendo experimentar con ellos de forma segura antes de trabajar con equipos físicos.
:::

---

## 24.1 La comunicación en una fábrica moderna

Si observamos una célula robotizada actual, comprobaremos que intervienen numerosos dispositivos.

Entre ellos podemos encontrar:

- un PLC encargado del control de la máquina;
- uno o varios robots industriales UR3;
- sensores y actuadores;
- cámaras de visión artificial;
- paneles HMI;
- sistemas SCADA;
- bases de datos;
- aplicaciones desarrolladas en Python;
- servidores de monitorización.

Todos estos elementos deben intercambiar información de forma continua.

La siguiente figura muestra un ejemplo simplificado de esta arquitectura.

::: figure
image: ../assets/cap24/fig24_1.png
caption: Arquitectura típica de comunicaciones en una célula robotizada industrial.
:::

Observa que el robot no constituye el centro del sistema.

Es únicamente uno de los numerosos dispositivos conectados a la red industrial.

Cada uno de ellos aporta una función específica y todos colaboran para automatizar el proceso de producción.

---

### Un ejemplo real

Imaginemos una célula robotizada encargada de clasificar piezas.

Cuando una pieza llega a la cinta transportadora, el proceso podría desarrollarse de la siguiente forma:

1. Un sensor detecta la llegada de la pieza.
2. El PLC recibe la señal y pone en marcha la secuencia automática.
3. Una cámara identifica el tipo de pieza.
4. El resultado se almacena en una base de datos.
5. El robot UR3 recoge la pieza y la deposita en la posición correspondiente.
6. El sistema SCADA actualiza el número de piezas procesadas.
7. Un panel HMI informa al operario del estado de la instalación.

Aunque para el usuario todo ocurre de forma transparente, internamente se están intercambiando cientos de mensajes por segundo.

Precisamente esos mensajes constituyen el objeto de estudio de este capítulo.

::: common-error
content:

Es frecuente pensar que el PLC controla directamente todos los dispositivos.

En realidad, muchos sistemas modernos funcionan mediante arquitecturas distribuidas donde PLC, robots, cámaras, aplicaciones y bases de datos colaboran intercambiando información mediante protocolos estandarizados.
:::

## 24.2 Principales protocolos de comunicación industrial

En la actualidad existen numerosos protocolos diseñados para intercambiar información entre dispositivos industriales.

Cada uno de ellos ha sido desarrollado para resolver necesidades diferentes.

Algunos están orientados al control de máquinas.

Otros facilitan la comunicación con aplicaciones web o servicios en la nube.

También existen protocolos especialmente diseñados para transmitir pequeñas cantidades de información con un consumo mínimo de recursos.

Durante este capítulo trabajaremos con cuatro de los más utilizados:

- **OPC UA**
- **MQTT**
- **TCP/IP**
- **REST API**

La siguiente figura muestra el ámbito de aplicación de cada uno de ellos.

::: figure
image: ../assets/cap24/fig24_2.png
caption: Protocolos de comunicación utilizados habitualmente en la Industria 4.0.
:::

Aunque todos permiten intercambiar información, cada protocolo presenta características diferentes.

Elegir el más adecuado dependerá siempre del tipo de aplicación que estemos desarrollando.

---

## OPC UA

**OPC UA** (*Open Platform Communications Unified Architecture*) es uno de los estándares más utilizados en automatización industrial.

Su principal objetivo consiste en permitir que equipos de diferentes fabricantes puedan comunicarse entre sí utilizando un lenguaje común.

Gracias a OPC UA es posible intercambiar información entre:

- PLC.
- Robots industriales.
- Sistemas SCADA.
- Bases de datos.
- Aplicaciones Python.
- Gemelos digitales.
- Plataformas de supervisión.

Una de sus principales ventajas consiste en que incorpora mecanismos de seguridad, autenticación y cifrado de la información.

Por este motivo se ha convertido en uno de los protocolos más utilizados en la Industria 4.0.

En capítulos posteriores utilizaremos OPC UA para comunicar CoppeliaSim con un PLC industrial.

---

## MQTT

**MQTT** (*Message Queuing Telemetry Transport*) es un protocolo diseñado para transmitir información de forma muy ligera y eficiente.

Su funcionamiento se basa en un modelo de **publicación y suscripción**, muy parecido al estudiado anteriormente en ROS 2.

En lugar de enviar información directamente entre dos aplicaciones, los mensajes se publican en un servidor denominado **broker**.

Los clientes interesados se suscriben a los temas (*topics*) que desean recibir.

La siguiente figura representa este mecanismo.

::: figure
image: ../assets/cap24/fig24_3.png
caption: Arquitectura de comunicación basada en MQTT.
:::

MQTT resulta especialmente útil para:

- sensores IoT;
- monitorización remota;
- sistemas domóticos;
- aplicaciones industriales distribuidas;
- comunicaciones con servicios en la nube.

Gracias a su reducido consumo de ancho de banda puede utilizarse incluso sobre conexiones de baja velocidad.

::: teacher
content:

Aprovecha para recordar al alumnado que el concepto de publicación y suscripción ya apareció en el capítulo anterior al estudiar ROS 2.

Aunque MQTT y ROS 2 son tecnologías diferentes, ambos utilizan una filosofía de comunicación muy similar.
:::

---

## TCP/IP

Todos los protocolos estudiados en este capítulo utilizan, de una forma u otra, la pila de comunicaciones **TCP/IP**.

TCP/IP constituye la base de prácticamente todas las redes informáticas actuales.

Su función consiste en garantizar que los datos lleguen correctamente desde un dispositivo hasta otro.

En una fábrica moderna encontramos redes TCP/IP conectando:

- PLC.
- Robots.
- Cámaras industriales.
- Ordenadores.
- Servidores.
- Paneles HMI.

Aunque normalmente trabajaremos con protocolos de nivel superior como OPC UA o MQTT, resulta importante comprender que todos ellos utilizan TCP/IP como infraestructura de transporte.

---

## REST API

Las aplicaciones modernas intercambian información con frecuencia mediante **REST API**.

Una REST API permite acceder a servicios remotos utilizando peticiones HTTP.

Gracias a este mecanismo es posible:

- consultar bases de datos;
- enviar órdenes a un servidor;
- obtener información desde aplicaciones web;
- integrar CoppeliaSim con plataformas externas.

Las REST API son muy habituales cuando un sistema industrial necesita comunicarse con aplicaciones desarrolladas para Internet o con servicios alojados en la nube.

::: common-error
content:

No confundas un protocolo de comunicación con una aplicación.

OPC UA, MQTT, TCP/IP y REST API son mecanismos para intercambiar información.

Cada uno está pensado para resolver un tipo diferente de problema.
:::

---

## ¿Qué protocolo utilizaremos?

A lo largo de esta parte del libro emplearemos los cuatro protocolos en diferentes situaciones.

En términos generales utilizaremos:

- **OPC UA** para comunicarnos con PLC y dispositivos industriales.
- **MQTT** para intercambiar información mediante publicación y suscripción.
- **TCP/IP** como infraestructura de comunicación.
- **REST API** para conectar CoppeliaSim con aplicaciones y servicios externos.

En el siguiente apartado comenzaremos estudiando con mayor profundidad **OPC UA**, el protocolo más utilizado actualmente en automatización industrial.

## 24.3 OPC UA: el estándar de la automatización industrial

Entre todos los protocolos utilizados actualmente en la industria, **OPC UA** ocupa un lugar especialmente importante.

Su objetivo consiste en permitir que dispositivos de diferentes fabricantes puedan intercambiar información de forma segura y estandarizada.

Antes de la aparición de OPC UA, cada fabricante utilizaba sus propios protocolos de comunicación.

Esto dificultaba enormemente la integración de equipos pertenecientes a marcas diferentes.

Con OPC UA este problema desaparece.

Todos los dispositivos hablan un mismo lenguaje.

Gracias a ello es posible conectar, por ejemplo:

- un PLC Omron;
- un robot UR3;
- una cámara industrial;
- un sistema SCADA;
- una aplicación Python;
- una base de datos;
- un simulador como CoppeliaSim.

Todos ellos pueden compartir información utilizando el mismo protocolo.

La siguiente figura muestra una arquitectura típica basada en OPC UA.

::: figure
image: ../assets/cap24/fig24_4.png
caption: Arquitectura cliente-servidor basada en OPC UA.
:::

---

## Arquitectura cliente-servidor

OPC UA utiliza un modelo **cliente-servidor**.

Este modelo ya apareció en el capítulo 22 cuando estudiamos la API remota de CoppeliaSim.

En este caso el funcionamiento es muy parecido.

Existe un dispositivo que ofrece información.

Ese dispositivo recibe el nombre de **servidor OPC UA**.

Por otra parte encontramos una o varias aplicaciones que solicitan dicha información.

Estas aplicaciones reciben el nombre de **clientes OPC UA**.

El intercambio de información siempre comienza cuando un cliente realiza una petición al servidor.

El servidor procesa la solicitud y devuelve la respuesta correspondiente.

Esta arquitectura facilita enormemente el intercambio de información entre dispositivos industriales.

---

### Ejemplo industrial

Imaginemos una célula robotizada formada por:

- un PLC Omron NX102;
- un robot UR3;
- una cámara industrial;
- CoppeliaSim;
- una aplicación Python.

En este escenario el PLC puede actuar como servidor OPC UA.

La aplicación Python se conecta como cliente y consulta diferentes variables del proceso.

Entre ellas podrían encontrarse:

- estado de la cinta transportadora;
- presencia de una pieza;
- velocidad del sistema;
- contador de producción;
- señal de inicio de ciclo.

Cada vez que el programa necesita conocer el estado del proceso, simplemente solicita la información al servidor OPC UA.

::: teacher
content:

Es recomendable insistir en que un cliente OPC UA no necesita conocer cómo está programado el PLC.

Únicamente necesita conocer qué variables ofrece el servidor y cómo acceder a ellas.

Esta independencia constituye una de las principales ventajas del protocolo.
:::

---

## 24.4 Variables y nodos OPC UA

Toda la información compartida mediante OPC UA se organiza en forma de **nodos**.

Cada nodo representa un elemento del sistema.

Un nodo puede contener:

- una variable;
- un objeto;
- un método;
- una alarma;
- un evento.

En este libro trabajaremos principalmente con variables.

Por ejemplo:

| Variable | Descripción |
|----------|-------------|
| `Robot_Ready` | Robot preparado para iniciar el ciclo. |
| `Start_Cycle` | Orden de inicio enviada por el PLC. |
| `Piece_Detected` | Sensor de presencia activado. |
| `Conveyor_Speed` | Velocidad de la cinta transportadora. |
| `Piece_Count` | Número de piezas procesadas. |

Cada una de estas variables puede ser leída o modificada desde una aplicación cliente, siempre que el servidor lo permita.

La siguiente figura representa un espacio de direcciones OPC UA simplificado.

::: figure
image: ../assets/cap24/fig24_5.png
caption: Organización de variables dentro del espacio de direcciones de un servidor OPC UA.
:::

---

### El espacio de direcciones

Todos los nodos disponibles en un servidor OPC UA forman el denominado **espacio de direcciones** (*Address Space*).

Podemos imaginarlo como un árbol donde cada rama representa un conjunto de información.

Por ejemplo:

```text
Servidor OPC UA
│
├── Robot
│   ├── Robot_Ready
│   ├── Position_X
│   ├── Position_Y
│   └── Position_Z
│
├── Cinta
│   ├── Conveyor_Speed
│   └── Motor_Status
│
└── Producción
    ├── Piece_Count
    └── Alarm_Status
```

Gracias a esta organización resulta muy sencillo localizar cualquier variable del sistema.

Además, los clientes pueden explorar automáticamente el espacio de direcciones sin necesidad de conocer previamente toda su estructura.

::: common-error
content:

Es frecuente pensar que las variables OPC UA son simples direcciones de memoria.

En realidad, cada variable forma parte de un modelo de información mucho más rico que incluye nombre, tipo de dato, permisos de acceso, descripción y otros metadatos.

Esta es una de las grandes diferencias entre OPC UA y otros protocolos industriales más antiguos.
:::

---

## ¿Por qué OPC UA se ha convertido en un estándar?

OPC UA ofrece numerosas ventajas frente a protocolos tradicionales.

Entre las más importantes destacan:

- independencia del fabricante;
- comunicación segura mediante cifrado;
- autenticación de usuarios;
- organización jerárquica de la información;
- posibilidad de acceder desde múltiples lenguajes de programación;
- compatibilidad con sistemas locales y servicios en la nube.

Gracias a estas características, actualmente es uno de los protocolos más utilizados para integrar robots, PLC, sistemas SCADA, aplicaciones Python y plataformas de Industria 4.0.

En el siguiente apartado aprenderemos a conectar una aplicación Python con un servidor OPC UA y leeremos nuestras primeras variables desde CoppeliaSim.
## 24.5 Preparando el entorno OPC UA

Después de comprender cómo funciona la arquitectura cliente-servidor de OPC UA, ha llegado el momento de realizar nuestra primera conexión desde Python.

Durante este capítulo utilizaremos el siguiente entorno de trabajo:

- CoppeliaSim EDU 4.10.
- Visual Studio Code.
- Python 3.
- Biblioteca `opcua` para Python.
- Un servidor OPC UA de pruebas.

En capítulos posteriores sustituiremos este servidor por un PLC industrial, pero para comenzar resulta mucho más sencillo trabajar con un entorno controlado.

La siguiente figura muestra la arquitectura que utilizaremos.

::: figure
image: ../assets/cap24/fig24_6.png
caption: Entorno de desarrollo para aplicaciones OPC UA con Python y CoppeliaSim.
:::

---

### Instalación de la biblioteca OPC UA

La comunicación con un servidor OPC UA requiere instalar previamente la biblioteca correspondiente.

Desde la terminal de Visual Studio Code ejecuta el siguiente comando:

```bash
pip install opcua
```

Una vez completada la instalación podremos acceder desde Python a cualquier servidor OPC UA compatible.

---

### Comprobando la instalación

Podemos verificar que la instalación ha sido correcta ejecutando el siguiente programa.

```python
from opcua import Client

print("Biblioteca OPC UA instalada correctamente.")
```

Si el programa se ejecuta sin errores, el entorno ya está preparado para comenzar a trabajar.

::: teacher
content:

Es recomendable comprobar la instalación en todos los equipos antes de iniciar las prácticas.

La mayoría de incidencias en este punto suelen deberse a que la biblioteca se ha instalado en un intérprete de Python diferente al utilizado por Visual Studio Code.
:::

---

## 24.6 Primera conexión desde Python

Una vez preparado el entorno podemos establecer la primera conexión con un servidor OPC UA.

El siguiente ejemplo muestra la estructura básica de un cliente.

```python
from opcua import Client

url = "opc.tcp://localhost:4840"

cliente = Client(url)

cliente.connect()

print("Conexión establecida correctamente.")

cliente.disconnect()
```

Aunque este ejemplo todavía no lee ninguna variable, ya incorpora las operaciones fundamentales que realizaremos en cualquier aplicación OPC UA.

El proceso siempre será el mismo:

1. Crear el cliente.
2. Indicar la dirección del servidor.
3. Establecer la conexión.
4. Intercambiar información.
5. Cerrar la conexión.

La siguiente figura resume este flujo de trabajo.

::: figure
image: ../assets/cap24/fig24_7.png
caption: Flujo básico de una conexión OPC UA desde una aplicación Python.
:::

---

### Analizando el código

La instrucción:

```python
Client(url)
```

crea un cliente OPC UA preparado para comunicarse con el servidor indicado.

Posteriormente:

```python
cliente.connect()
```

establece la conexión física.

A partir de ese momento podremos acceder a las variables disponibles en el servidor.

Finalmente:

```python
cliente.disconnect()
```

libera todos los recursos utilizados y cierra correctamente la sesión.

Cerrar siempre la conexión constituye una buena práctica de programación y evita dejar sesiones abiertas innecesariamente.

::: common-error
content:

Un error muy frecuente consiste en olvidar llamar al método `disconnect()`.

Aunque el programa finalice correctamente, el servidor puede mantener la sesión abierta durante un tiempo, consumiendo recursos de forma innecesaria.
:::

---

## Preparando la lectura de variables

Ya somos capaces de establecer una conexión con un servidor OPC UA.

En el siguiente apartado aprenderemos a localizar variables dentro del espacio de direcciones, leer su contenido y modificar su valor desde Python.

A partir de ese momento comenzaremos a intercambiar información entre CoppeliaSim, aplicaciones Python y dispositivos industriales siguiendo exactamente el mismo procedimiento utilizado en sistemas reales.

## 24.7 Lectura y escritura de variables OPC UA

Una vez establecida la conexión con el servidor OPC UA, el siguiente paso consiste en acceder a las variables que forman parte de su espacio de direcciones.

Estas variables representan el estado del proceso industrial y permiten intercambiar información entre diferentes dispositivos.

En nuestro ejemplo simularemos una instalación formada por:

- un PLC Omron NX102;
- una aplicación Python;
- CoppeliaSim;
- un robot UR3.

La aplicación Python actuará como cliente OPC UA y consultará el estado de diferentes variables del proceso.

La siguiente figura representa este intercambio de información.

::: figure
image: ../assets/cap24/fig24_8.png
caption: Lectura y escritura de variables mediante un cliente OPC UA.
:::

---

### Leyendo una variable

El siguiente programa muestra cómo acceder al valor de una variable del servidor.

```python
from opcua import Client

url = "opc.tcp://localhost:4840"

cliente = Client(url)
cliente.connect()

nodo = cliente.get_node("ns=2;i=2")

valor = nodo.get_value()

print("Valor recibido:", valor)

cliente.disconnect()
```

El procedimiento es muy sencillo:

1. Conectarse al servidor.
2. Obtener una referencia al nodo.
3. Leer su valor.
4. Mostrar el resultado.
5. Cerrar la conexión.

---

### Modificando una variable

Además de leer información, un cliente OPC UA también puede modificar determinadas variables, siempre que el servidor lo permita.

```python
from opcua import ua

nodo.set_value(ua.DataValue(True))
```

Este mecanismo resulta muy útil para:

- iniciar un ciclo automático;
- activar un actuador;
- enviar órdenes a un PLC;
- modificar parámetros de funcionamiento.

En aplicaciones reales será habitual combinar continuamente operaciones de lectura y escritura.

::: teacher
content:

Explica al alumnado que no todas las variables pueden modificarse.

En muchos servidores OPC UA existen variables de solo lectura cuyo objetivo es proporcionar información del proceso sin permitir cambios desde el exterior.
:::

---

## Integrando OPC UA con CoppeliaSim

Una vez dominadas las operaciones básicas, podemos utilizar OPC UA para comunicar CoppeliaSim con aplicaciones externas.

Un ejemplo típico consiste en sincronizar una simulación con un PLC industrial.

El funcionamiento general sería el siguiente:

1. El PLC detecta una pieza mediante un sensor.
2. Publica el estado de la variable `Piece_Detected`.
3. Python lee dicha variable mediante OPC UA.
4. Python ordena a CoppeliaSim iniciar el movimiento del robot UR3.
5. El robot recoge la pieza en la simulación.
6. Python actualiza el contador de producción en el PLC.

La siguiente figura representa este flujo de información.

::: figure
image: ../assets/cap24/fig24_9.png
caption: Integración de un PLC, Python y CoppeliaSim mediante OPC UA.
:::

Este tipo de arquitectura constituye la base de numerosos gemelos digitales utilizados actualmente en la industria.

---

## Buenas prácticas

Cuando desarrolles aplicaciones OPC UA procura seguir siempre estas recomendaciones:

- cerrar correctamente las conexiones;
- comprobar posibles errores de comunicación;
- documentar el significado de cada variable;
- utilizar nombres descriptivos;
- evitar accesos innecesarios al servidor;
- proteger las comunicaciones mediante autenticación y cifrado cuando el entorno lo requiera.

Estas prácticas mejoran la fiabilidad de las aplicaciones y facilitan su mantenimiento.

::: common-error
content:

No accedas continuamente a una misma variable si no es necesario.

Las consultas excesivas pueden aumentar el tráfico de red y reducir el rendimiento del sistema, especialmente cuando intervienen numerosos clientes simultáneamente.
:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| OPC UA | Estándar de comunicación para automatización industrial. |
| Cliente OPC UA | Aplicación que solicita información al servidor. |
| Servidor OPC UA | Dispositivo que ofrece variables y servicios. |
| Espacio de direcciones | Organización jerárquica de todos los nodos del servidor. |
| Nodo | Elemento del espacio de direcciones que representa una variable, objeto o método. |
| Variable | Información compartida entre los distintos dispositivos. |
| PLC | Controlador lógico programable encargado del control de la instalación. |
| Gemelo digital | Representación virtual sincronizada con un sistema físico. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender el funcionamiento de OPC UA.
- ✅ Diferenciar clientes y servidores OPC UA.
- ✅ Interpretar un espacio de direcciones.
- ✅ Crear un cliente OPC UA utilizando Python.
- ✅ Leer y escribir variables de un servidor.
- ✅ Comprender cómo integrar CoppeliaSim con un PLC mediante OPC UA.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué función desempeña un servidor OPC UA?
2. ¿Qué diferencia existe entre un cliente y un servidor?
3. ¿Qué es el espacio de direcciones?
4. ¿Cómo se obtiene una referencia a una variable desde Python?
5. ¿Qué método permite leer el contenido de un nodo?
6. ¿Qué ventajas ofrece OPC UA frente a protocolos propietarios?
7. ¿Qué papel desempeña Python al integrar CoppeliaSim con un PLC?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a desarrollar aplicaciones industriales conectadas.

---

## Práctica guiada

::: practice
title: Primera aplicación OPC UA con Python

difficulty: Media

time: 60 minutos

content:

Realiza las siguientes tareas.

1. Instala la biblioteca `opcua`.
2. Comprueba que el servidor OPC UA está disponible.
3. Conéctate desde Python.
4. Lee el valor de una variable.
5. Muestra el resultado por pantalla.
6. Modifica una variable de escritura.
7. Comprueba el cambio desde el servidor.
8. Cierra correctamente la conexión.
9. Repite el proceso varias veces.
10. Analiza el tráfico de información intercambiado.

El objetivo consiste en comprender el ciclo completo de comunicación mediante OPC UA.

:::

---

## Reto

::: challenge
title: Diseñando un sistema industrial conectado

content:

Diseña una arquitectura basada en OPC UA para una célula robotizada formada por:

- un PLC;
- un robot UR3;
- una cámara industrial;
- una aplicación Python;
- una base de datos.

Indica:

- qué dispositivo actuará como servidor;
- qué aplicaciones serán clientes;
- qué variables deberían compartirse;
- qué información sería de solo lectura y cuál permitiría escritura.

Realiza un esquema del sistema y justifica tus decisiones.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento de OPC UA.
- Crear un cliente utilizando Python.
- Leer y escribir variables industriales.
- Entender la integración entre PLC, Python y CoppeliaSim.

**Material necesario**

- Visual Studio Code.
- Python 3.x.
- Biblioteca `opcua`.
- CoppeliaSim EDU 4.10.
- Servidor OPC UA de pruebas o PLC Omron NX102.

**Consejos metodológicos**

Siempre que sea posible, muestra primero el funcionamiento con un servidor de pruebas y posteriormente repite la práctica utilizando un PLC real.

El alumnado comprenderá mucho mejor que los mismos programas pueden utilizarse tanto en simulación como en una instalación industrial.

:::

---

## Próximo capítulo

En este punto ya somos capaces de comunicar aplicaciones Python con sistemas industriales mediante OPC UA.

En el siguiente capítulo daremos un paso más y construiremos un **gemelo digital**, sincronizando en tiempo real una instalación física con su representación en CoppeliaSim.

Aprenderemos conceptos como sincronización, monitorización, trazabilidad, bases de datos y paneles de supervisión, acercándonos al funcionamiento de una auténtica solución de **Industria 4.0**.
