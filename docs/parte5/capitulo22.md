::: chapter-cover
number: 22
title: Comunicación entre CoppeliaSim y aplicaciones externas
time: 4 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se comunica CoppeliaSim con aplicaciones externas.
- Diferenciar una arquitectura cliente-servidor de una aplicación monolítica.
- Entender el funcionamiento de la API remota de CoppeliaSim.
- Identificar el flujo de intercambio de información entre Python y el simulador.
- Preparar el entorno para desarrollar aplicaciones distribuidas.
:::

# Capítulo 22 · Comunicación entre CoppeliaSim y aplicaciones externas

## ¿Por qué comunicar CoppeliaSim con otros programas?

Hasta ahora hemos trabajado con CoppeliaSim como una aplicación prácticamente autónoma.

Hemos creado escenas, añadido robots, programado comportamientos y utilizado sensores y cámaras para resolver diferentes problemas de robótica.

Sin embargo, en un entorno industrial real un robot nunca trabaja de forma aislada.

Forma parte de un sistema mucho más amplio donde intercambia información continuamente con otros dispositivos y aplicaciones.

Por ejemplo, un robot puede recibir órdenes desde un sistema de planificación, enviar el estado de una operación a una base de datos, consultar un PLC para conocer el estado de una máquina o transmitir imágenes a un servidor encargado de realizar visión artificial.

En otras palabras, el robot es únicamente uno de los elementos que forman parte de una arquitectura distribuida.

Precisamente esa será la finalidad de esta parte del libro.

Aprenderemos a integrar CoppeliaSim dentro de aplicaciones reales utilizando Python como lenguaje de comunicación.

Comenzaremos intercambiando información con programas sencillos y, progresivamente, construiremos sistemas similares a los utilizados actualmente en la Industria 4.0.

::: teacher
content:

Antes de comenzar con la programación conviene insistir en que, a partir de este capítulo, CoppeliaSim dejará de ser una aplicación independiente para convertirse en un componente más de un sistema distribuido.

Este cambio de perspectiva ayuda al alumnado a comprender mejor la arquitectura utilizada en la automatización industrial moderna.
:::

---

## 22.1 ¿Qué significa comunicar dos aplicaciones?

Cuando hablamos de comunicación entre aplicaciones nos referimos al proceso mediante el cual dos programas diferentes intercambian información para colaborar en la resolución de una tarea.

Cada aplicación ejecuta una parte del trabajo y comparte únicamente los datos necesarios.

Este enfoque presenta numerosas ventajas.

Permite distribuir el procesamiento entre distintos equipos, reutilizar aplicaciones ya desarrolladas y facilitar el mantenimiento del sistema.

En nuestro caso tendremos dos protagonistas principales:

- **CoppeliaSim**, encargado de simular el robot y su entorno.
- **Python**, encargado de ejecutar la lógica de control.

Ambos programas podrán ejecutarse en el mismo ordenador o en equipos diferentes conectados mediante una red.

La forma en que intercambian información será prácticamente la misma.

La siguiente figura representa esta arquitectura básica.

::: figure
image: ../assets/cap22/fig22_1.png
caption: Arquitectura básica de comunicación entre una aplicación Python y CoppeliaSim.
:::

Observa que ninguno de los dos programas controla directamente al otro.

Ambos permanecen en ejecución y se comunican mediante mensajes.

Esta filosofía será la base de todos los capítulos de esta parte del libro.

---

### Una analogía sencilla

Podemos imaginar esta comunicación como una conversación telefónica entre dos personas.

Cada una realiza una función distinta.

Una persona hace preguntas.

La otra responde.

Del mismo modo, un programa Python puede solicitar información sobre la posición de un robot y CoppeliaSim responder con las coordenadas correspondientes.

Posteriormente Python puede calcular una nueva trayectoria y enviar otra orden al simulador para mover el robot.

Durante toda la ejecución ambos programas permanecen intercambiando mensajes de forma continua.

Este mecanismo resulta mucho más flexible que integrar toda la lógica dentro de una única aplicación.

::: common-error
content:

Es habitual pensar que Python "controla" completamente CoppeliaSim.

En realidad ambos programas son independientes.

Python únicamente envía solicitudes y procesa las respuestas que recibe del simulador.
:::

## 22.2 Arquitectura cliente-servidor

La mayoría de las aplicaciones distribuidas modernas utilizan una arquitectura denominada **cliente-servidor**.

Aunque el nombre pueda parecer complejo, el concepto es muy sencillo.

Un programa, denominado **cliente**, realiza una petición.

Otro programa, denominado **servidor**, recibe esa petición, la procesa y devuelve una respuesta.

Este intercambio puede repetirse cientos o incluso miles de veces por segundo.

En nuestro caso:

- **Python** actuará como cliente.
- **CoppeliaSim** actuará como servidor.

Python enviará órdenes como:

- obtener la posición de un robot;
- leer un sensor;
- mover una articulación;
- iniciar una simulación.

CoppeliaSim procesará cada solicitud y responderá con la información correspondiente.

La siguiente figura resume esta arquitectura.

::: figure
image: ../assets/cap22/fig22_2.png
caption: Arquitectura cliente-servidor utilizada por CoppeliaSim y Python.
:::

Observa que ambos programas permanecen funcionando simultáneamente.

Ninguno necesita conocer cómo está implementado internamente el otro.

Únicamente deben compartir un mismo protocolo de comunicación.

Esta independencia constituye una de las mayores ventajas de este tipo de arquitecturas.

---

### Cliente y servidor intercambian mensajes

Cuando Python necesita conocer el estado de un sensor no accede directamente a la memoria de CoppeliaSim.

En su lugar envía un mensaje.

Podemos imaginar el proceso de la siguiente manera:

1. Python solicita la lectura de un sensor.
2. CoppeliaSim recibe la petición.
3. El simulador obtiene el valor solicitado.
4. Devuelve la respuesta a Python.
5. Python continúa ejecutando el programa utilizando esa información.

Todo este proceso suele completarse en apenas unos milisegundos.

Para el programador parece que ambos programas trabajan como si fueran una única aplicación.

---

## 22.3 La API remota

Para que dos programas puedan entenderse necesitan utilizar un mismo lenguaje de comunicación.

Ese conjunto de funciones recibe el nombre de **API** (*Application Programming Interface*).

Una API define:

- qué operaciones pueden realizarse;
- qué datos deben enviarse;
- cómo se reciben las respuestas;
- qué ocurre cuando aparece un error.

CoppeliaSim incorpora varias APIs.

La que utilizaremos durante este capítulo será la **API remota**, diseñada específicamente para permitir que aplicaciones externas controlen la simulación.

Gracias a esta API podremos:

- iniciar y detener una simulación;
- obtener información de sensores;
- mover robots;
- modificar objetos;
- crear escenas dinámicamente;
- intercambiar datos con Python.

Todo ello sin necesidad de escribir scripts dentro del propio simulador.

La siguiente figura muestra el papel que desempeña la API remota entre ambas aplicaciones.

::: figure
image: ../assets/cap22/fig22_3.png
caption: La API remota actúa como intermediaria entre Python y CoppeliaSim.
:::

::: teacher
content:

Antes de mostrar ejemplos de programación resulta recomendable insistir en que la API no es un programa adicional, sino un conjunto de funciones que ambos extremos conocen y utilizan para comunicarse de forma estandarizada.

Muchos estudiantes comprenden mejor este concepto si se compara con el funcionamiento de una API web utilizada por aplicaciones móviles.
:::

---

### ¿Qué ventajas ofrece una API?

Utilizar una API aporta numerosas ventajas frente a acceder directamente al simulador.

Entre las más importantes destacan:

- independencia entre aplicaciones;
- mayor facilidad para reutilizar código;
- posibilidad de distribuir el procesamiento entre varios equipos;
- compatibilidad con diferentes lenguajes de programación;
- mantenimiento más sencillo.

Gracias a estas características podremos desarrollar programas cada vez más complejos sin modificar el funcionamiento interno de CoppeliaSim.

---

## 22.4 Un primer flujo de comunicación

Aunque todavía no escribiremos código, ya podemos comprender cómo será el funcionamiento general de nuestras aplicaciones.

El proceso seguirá siempre una secuencia muy parecida:

1. Python establece la conexión con CoppeliaSim.
2. El simulador acepta la conexión.
3. Python solicita una operación.
4. CoppeliaSim ejecuta dicha operación.
5. El simulador devuelve el resultado.
6. Python decide cuál será la siguiente acción.

Este ciclo se repetirá continuamente durante toda la ejecución del programa.

En los próximos apartados aprenderemos cómo implementar este flujo utilizando Python y la API remota.

## 22.5 Intercambio de datos entre Python y CoppeliaSim

Una vez establecida la conexión entre ambas aplicaciones, el siguiente paso consiste en intercambiar información.

Toda la comunicación entre Python y CoppeliaSim se basa en un principio muy sencillo:

> **Python solicita información o envía órdenes, y CoppeliaSim responde ejecutando la acción solicitada o devolviendo los datos correspondientes.**

Aunque internamente este proceso resulta muy complejo, para el programador se reduce a utilizar funciones proporcionadas por la API remota.

Estas funciones permiten acceder prácticamente a cualquier elemento de la simulación.

Por ejemplo, podremos:

- obtener la posición de un robot;
- leer el estado de un sensor;
- mover una articulación;
- modificar la orientación de un objeto;
- iniciar o detener la simulación;
- consultar variables internas.

La siguiente figura resume el flujo de intercambio de información.

::: figure
image: ../assets/cap22/fig22_4.png
caption: Flujo de intercambio de datos entre Python y CoppeliaSim.
:::

---

### Tipos de datos intercambiados

No toda la información tiene el mismo formato.

Dependiendo de la operación realizada, la API remota puede intercambiar distintos tipos de datos.

Los más habituales son:

| Tipo de dato | Ejemplo |
|--------------|---------|
| Enteros | Identificador de un objeto |
| Reales | Posición, velocidad o distancia |
| Booleanos | Sensor activado o desactivado |
| Texto | Nombre de un objeto |
| Listas | Coordenadas cartesianas |
| Imágenes | Captura de una cámara de visión |

Durante los próximos capítulos trabajaremos con todos ellos.

---

## 22.6 Variables compartidas

En muchas ocasiones necesitaremos que Python y CoppeliaSim compartan información de forma continua.

Imaginemos un programa que controla una cinta transportadora.

Mientras CoppeliaSim simula el movimiento de la cinta, Python debe conocer constantemente:

- la velocidad actual;
- la posición de una pieza;
- el estado de un sensor;
- el instante en que una pieza llega al final del recorrido.

Para conseguirlo ambas aplicaciones intercambian variables continuamente.

No es necesario que Python conozca todos los detalles internos del simulador.

Únicamente solicita las variables que necesita en cada instante.

Este mecanismo reduce considerablemente la cantidad de información transmitida y mejora el rendimiento de la aplicación.

La siguiente figura representa este intercambio continuo de variables.

::: figure
image: ../assets/cap22/fig22_5.png
caption: Variables compartidas entre Python y CoppeliaSim.
:::

::: teacher
content:

Es importante transmitir al alumnado que las variables no "viven" simultáneamente en ambos programas.

Cada aplicación mantiene sus propias variables y únicamente intercambia los valores necesarios mediante la API remota.

Comprender esta diferencia facilitará posteriormente el trabajo con ROS 2, MQTT y OPC UA.
:::

---

## 22.7 Sincronización entre aplicaciones

Intercambiar datos no siempre es suficiente.

También es necesario asegurarse de que ambas aplicaciones trabajan de forma coordinada.

Supongamos que Python solicita la posición de un robot justo antes de que CoppeliaSim actualice la simulación.

La información obtenida podría no corresponder exactamente con el estado más reciente del robot.

Para evitar este tipo de situaciones es necesario sincronizar ambos programas.

En términos generales, la sincronización consiste en garantizar que las operaciones se realizan en el momento adecuado.

Gracias a ello conseguiremos:

- evitar lecturas inconsistentes;
- coordinar movimientos complejos;
- mantener la simulación estable;
- obtener resultados reproducibles.

En capítulos posteriores veremos cómo controlar esta sincronización de forma precisa utilizando las funciones de la API remota.

::: common-error
content:

Un error muy frecuente consiste en asumir que Python y CoppeliaSim ejecutan cada instrucción exactamente al mismo tiempo.

En realidad, ambos programas trabajan de forma independiente y la sincronización debe gestionarse explícitamente cuando la aplicación lo requiere.
:::

---

### Preparando la primera práctica

Ya conocemos los conceptos fundamentales necesarios para comenzar a trabajar.

En el siguiente apartado realizaremos nuestra primera conexión entre Python y CoppeliaSim utilizando la API remota.

Será el primer programa de esta parte del libro y servirá como base para todas las aplicaciones que desarrollaremos a continuación.

## 22.8 Preparando el entorno de trabajo

Después de comprender cómo se comunican Python y CoppeliaSim, ha llegado el momento de establecer nuestra primera conexión real entre ambas aplicaciones.

En este capítulo utilizaremos exactamente el mismo entorno de desarrollo que hemos empleado a lo largo del libro:

- CoppeliaSim EDU 4.10.
- Visual Studio Code.
- Python 3.
- La API remota integrada en CoppeliaSim.

El objetivo consistirá en ejecutar un programa Python desde Visual Studio Code que se comunique con una simulación en ejecución.

A partir de este momento trabajaremos siempre con dos aplicaciones abiertas simultáneamente:

- **CoppeliaSim**, donde se ejecutará la simulación.
- **Visual Studio Code**, desde donde desarrollaremos y ejecutaremos nuestros programas Python.

La siguiente figura muestra el entorno de trabajo que utilizaremos durante el resto de esta parte del libro.

::: figure
image: ../assets/cap22/fig22_6.png
caption: Entorno de trabajo utilizado para desarrollar aplicaciones con Python y CoppeliaSim.
:::

---

## Comprobando la instalación

Antes de comenzar conviene verificar que todo el software funciona correctamente.

Comprueba los siguientes puntos:

- CoppeliaSim se abre sin errores.
- Visual Studio Code reconoce el intérprete de Python.
- El proyecto dispone de un entorno virtual configurado (opcional, pero recomendable).
- La simulación puede iniciarse y detenerse correctamente.

Si alguno de estos elementos no funciona, es recomendable resolver el problema antes de continuar.

Una configuración correcta evitará numerosos errores durante las prácticas posteriores.

::: teacher
content:

Es recomendable dedicar unos minutos al inicio de la sesión para comprobar que todos los equipos del aula disponen de la misma versión de CoppeliaSim y Python.

Esto evita diferencias de comportamiento entre alumnos y simplifica enormemente la resolución de incidencias.
:::

---

## 22.9 La API remota ZeroMQ

Las versiones actuales de CoppeliaSim incorporan una nueva API remota basada en **ZeroMQ**.

Esta API sustituye a la antigua Remote API utilizada en versiones anteriores del simulador y ofrece importantes mejoras en rendimiento, estabilidad y facilidad de uso.

Entre sus principales ventajas destacan:

- comunicación más rápida;
- menor latencia;
- mayor estabilidad;
- soporte para múltiples lenguajes de programación;
- arquitectura más sencilla.

Durante todo este libro utilizaremos exclusivamente esta API.

No será necesario instalar componentes adicionales, ya que CoppeliaSim incorpora el servidor ZeroMQ preparado para aceptar conexiones desde aplicaciones externas.

La siguiente figura representa la arquitectura utilizada.

::: figure
image: ../assets/cap22/fig22_7.png
caption: Arquitectura de comunicación mediante la API remota ZeroMQ.
:::

---

### ¿Cómo funciona ZeroMQ?

Cuando iniciamos una simulación, CoppeliaSim pone en funcionamiento un servidor de comunicaciones.

Nuestro programa Python actúa como cliente.

El proceso general será siempre el mismo:

1. Python crea una conexión con CoppeliaSim.
2. El servidor acepta la conexión.
3. Python solicita una operación.
4. CoppeliaSim ejecuta la petición.
5. El resultado vuelve al programa Python.

Todo este intercambio se realiza de forma prácticamente instantánea.

Desde el punto de vista del programador, basta con llamar a las funciones de la API para acceder a cualquier objeto de la simulación.

---

## Primer proyecto Python

Para mantener organizados todos los ejemplos del libro crearemos un nuevo proyecto.

La estructura recomendada será la siguiente:

```text
capitulo22/
│
├── main.py
├── requirements.txt
├── .venv/
└── README.md
```

Durante los próximos apartados iremos ampliando este proyecto con nuevos programas de ejemplo.

Cada uno de ellos mostrará una funcionalidad distinta de la API remota.

::: common-error
content:

No ejecutes el programa Python antes de iniciar CoppeliaSim.

Aunque el código sea correcto, la conexión no podrá establecerse si el simulador todavía no está preparado para aceptar peticiones.
:::

---

### En la siguiente sección...

Ya está todo preparado.

En el siguiente apartado escribiremos nuestro **primer programa Python** capaz de establecer una conexión con CoppeliaSim.

A partir de ese momento comenzaremos a controlar la simulación directamente desde Visual Studio Code, iniciando una nueva forma de desarrollar aplicaciones robóticas.

## 22.10 Nuestra primera conexión con CoppeliaSim

Ha llegado el momento de escribir nuestro primer programa.

El objetivo será comprobar que Python es capaz de establecer una conexión con CoppeliaSim y acceder a la simulación.

No moveremos todavía ningún robot.

Simplemente verificaremos que ambas aplicaciones pueden comunicarse correctamente.

### Instalando las bibliotecas necesarias

La API remota basada en ZeroMQ utiliza un pequeño paquete de Python.

Podemos instalarlo fácilmente desde el terminal de Visual Studio Code.

```bash
pip install coppeliasim-zmqremoteapi-client
```

Una vez finalizada la instalación ya podremos importar la biblioteca desde cualquier programa Python.

---

### Primer programa

Crea un archivo llamado **main.py** e introduce el siguiente código.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Crear el cliente
client = RemoteAPIClient()

# Obtener el objeto principal del simulador
sim = client.require('sim')

print("Conexión establecida correctamente.")
print(f"Tiempo actual de simulación: {sim.getSimulationTime():.3f} segundos")
```

Si CoppeliaSim está ejecutándose y la simulación se encuentra iniciada, el programa mostrará un resultado similar al siguiente:

```text
Conexión establecida correctamente.
Tiempo actual de simulación: 2.417 segundos
```

Aunque el ejemplo es muy sencillo, representa un paso muy importante.

Por primera vez nuestro programa Python ha conseguido acceder al simulador y obtener información en tiempo real.

A partir de este momento podremos controlar cualquier elemento de la escena.

---

## Analizando el programa

Veamos qué realiza cada una de las instrucciones anteriores.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
```

Importa la biblioteca que permite establecer la comunicación con CoppeliaSim.

---

```python
client = RemoteAPIClient()
```

Crea el cliente ZeroMQ encargado de comunicarse con el simulador.

---

```python
sim = client.require('sim')
```

Obtiene una referencia al objeto principal de la API de CoppeliaSim.

A través de esta referencia podremos acceder posteriormente a todas las funciones del simulador.

---

```python
sim.getSimulationTime()
```

Solicita al simulador el tiempo transcurrido desde el inicio de la simulación.

Es una función muy útil para comprobar que la comunicación funciona correctamente.

::: teacher
content:

Durante la práctica conviene pedir al alumnado que detenga la simulación y vuelva a ejecutar el programa.

De este modo comprobarán que el tiempo de simulación permanece detenido mientras CoppeliaSim no está ejecutándose, reforzando así la idea de que Python consulta información proporcionada por el simulador.
:::

---

## ¿Qué haremos a partir de ahora?

En los siguientes capítulos utilizaremos exactamente la misma conexión para realizar operaciones mucho más interesantes.

Por ejemplo, aprenderemos a:

- obtener la posición de un objeto;
- mover articulaciones del robot UR3;
- leer sensores;
- capturar imágenes;
- intercambiar datos con aplicaciones industriales;
- integrar CoppeliaSim con ROS 2 y protocolos como OPC UA y MQTT.

La conexión que hemos creado en este capítulo será la base de todas esas aplicaciones.

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Cliente | Aplicación que solicita servicios al simulador. |
| Servidor | Aplicación que procesa las solicitudes y devuelve respuestas. |
| API remota | Conjunto de funciones que permiten controlar CoppeliaSim desde aplicaciones externas. |
| ZeroMQ | Tecnología de comunicación utilizada por la API remota moderna de CoppeliaSim. |
| Cliente ZeroMQ | Objeto Python encargado de establecer la conexión con el simulador. |
| Variables compartidas | Información intercambiada entre Python y CoppeliaSim. |
| Sincronización | Coordinación temporal entre ambas aplicaciones. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender la arquitectura cliente-servidor utilizada por CoppeliaSim.
- ✅ Explicar el funcionamiento de la API remota.
- ✅ Comprender cómo se intercambian datos entre Python y el simulador.
- ✅ Preparar un entorno de desarrollo para aplicaciones distribuidas.
- ✅ Crear una conexión básica utilizando la API remota ZeroMQ.
- ✅ Obtener información del simulador desde un programa Python.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué papel desempeña Python en una arquitectura cliente-servidor?
2. ¿Qué función realiza CoppeliaSim durante la comunicación?
3. ¿Qué es una API remota?
4. ¿Qué ventajas ofrece ZeroMQ respecto a la antigua API remota?
5. ¿Qué función desempeña el objeto `RemoteAPIClient`?
6. ¿Cómo podemos comprobar que la conexión con CoppeliaSim se ha establecido correctamente?

Si puedes responder a todas ellas, estás preparado para comenzar a controlar la simulación desde Python.

---

## Práctica guiada

::: practice
title: Primera conexión con CoppeliaSim

difficulty: Baja

time: 30 minutos

content:

Realiza las siguientes tareas.

1. Inicia CoppeliaSim.
2. Carga una escena vacía.
3. Ejecuta la simulación.
4. Crea un proyecto Python en Visual Studio Code.
5. Instala el cliente ZeroMQ.
6. Escribe el programa mostrado en este capítulo.
7. Ejecuta el programa.
8. Comprueba que aparece el tiempo de simulación.
9. Detén la simulación y vuelve a ejecutar el programa.
10. Analiza las diferencias observadas.

El objetivo de la práctica es verificar que Python y CoppeliaSim pueden comunicarse correctamente.
:::

---

## Reto

::: challenge
title: Explorando la API remota

content:

Consulta la documentación oficial de la API remota de CoppeliaSim e identifica tres funciones adicionales del objeto `sim`.

Para cada una de ellas responde:

- ¿Qué información devuelve?
- ¿Qué parámetros necesita?
- ¿En qué aplicación robótica podría utilizarse?

Comparte tus conclusiones con el resto de la clase.

Este pequeño ejercicio te permitirá comenzar a familiarizarte con la enorme cantidad de funciones disponibles en la API.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Una sesión de 55 minutos.

**Objetivos**

- Comprender el modelo de comunicación cliente-servidor.
- Configurar el entorno de desarrollo.
- Establecer la primera conexión entre Python y CoppeliaSim.
- Interpretar el funcionamiento básico de la API remota.

**Material necesario**

- Ordenador con CoppeliaSim EDU 4.10 instalado.
- Visual Studio Code.
- Python 3.x.
- Acceso al terminal para instalar la biblioteca `coppeliasim-zmqremoteapi-client`.

**Consejos metodológicos**

No continúes con el siguiente capítulo hasta que todos los alumnos hayan conseguido establecer correctamente la conexión con el simulador.

Esta práctica constituye la base de toda la Parte V.
:::

---

## Próximo capítulo

Ya somos capaces de comunicar Python con CoppeliaSim.

En el siguiente capítulo daremos un paso más e integraremos el simulador con **ROS 2**, el estándar de comunicación utilizado actualmente en robótica.

Aprenderemos qué son los nodos, los *topics*, los publicadores y los suscriptores, desarrollando nuestras primeras aplicaciones robóticas distribuidas sobre una arquitectura profesional.