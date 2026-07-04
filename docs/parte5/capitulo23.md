::: chapter-cover
number: 23
title: Integración con ROS 2
time: 5 horas
level: ⭐⭐⭐⭐☆ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es ROS 2 y cuál es su papel en la robótica moderna.
- Identificar los principales componentes de una arquitectura ROS 2.
- Comprender el funcionamiento de nodos, topics, publicadores y suscriptores.
- Integrar CoppeliaSim dentro de una aplicación basada en ROS 2.
- Preparar el entorno de desarrollo para las primeras prácticas.
:::

# Capítulo 23 · Integración con ROS 2

## ¿Por qué aprender ROS 2?

Hasta este momento hemos utilizado CoppeliaSim como plataforma para desarrollar y probar aplicaciones robóticas mediante Python.

Hemos aprendido a controlar robots móviles, utilizar sensores, procesar imágenes, manipular objetos con un brazo industrial UR3 y comunicar el simulador con aplicaciones externas.

Sin embargo, los sistemas robóticos utilizados actualmente en la industria y en la investigación rara vez están formados por un único programa.

Lo habitual es encontrar múltiples aplicaciones trabajando de forma coordinada.

Por ejemplo:

- un programa controla el robot;
- otro procesa las imágenes de una cámara;
- un tercero planifica las trayectorias;
- un cuarto supervisa el estado del sistema;
- otro almacena información en una base de datos.

Cada una de estas aplicaciones puede ejecutarse incluso en ordenadores diferentes.

Para coordinar todo este ecosistema se utilizan plataformas de comunicación específicas.

La más extendida actualmente en robótica es **ROS 2** (*Robot Operating System 2*).

A pesar de su nombre, ROS 2 no es un sistema operativo.

Se trata de un conjunto de herramientas, bibliotecas y estándares que permiten desarrollar aplicaciones robóticas distribuidas de forma sencilla y organizada.

Gracias a ROS 2 diferentes programas pueden intercambiar información sin necesidad de conocer cómo están implementados internamente.

Esta filosofía facilita enormemente el desarrollo de sistemas complejos y permite reutilizar componentes desarrollados por otros equipos.

::: teacher
content:

Muchos estudiantes interpretan inicialmente que ROS 2 sustituye a Python o a CoppeliaSim.

Es importante insistir desde el principio en que ROS 2 no reemplaza estas herramientas.

Python seguirá siendo el lenguaje de programación principal y CoppeliaSim continuará actuando como simulador.

ROS 2 proporcionará la infraestructura de comunicación que permitirá coordinar todos los componentes del sistema.
:::

---

## 23.1 ¿Qué es ROS 2?

ROS 2 es un entorno de desarrollo diseñado específicamente para aplicaciones robóticas distribuidas.

Su principal objetivo consiste en facilitar la comunicación entre diferentes programas que colaboran para controlar un robot o un sistema automatizado.

En lugar de desarrollar una única aplicación enorme, ROS 2 propone dividir el sistema en pequeños módulos independientes.

Cada módulo realiza una tarea concreta.

Por ejemplo:

- controlar un robot UR3;
- adquirir imágenes de una cámara;
- detectar objetos mediante visión artificial;
- calcular trayectorias;
- supervisar sensores;
- comunicarse con un PLC.

Todos estos módulos intercambian información mediante mecanismos de comunicación estandarizados.

La siguiente figura muestra la idea general de una arquitectura basada en ROS 2.

::: figure
image: ../assets/cap23/fig23_1.png
caption: Arquitectura general de una aplicación robótica basada en ROS 2.
:::

Observa que ningún módulo controla directamente al resto.

Cada componente realiza una función específica y se comunica con los demás utilizando los mecanismos proporcionados por ROS 2.

Esta arquitectura ofrece importantes ventajas:

- facilita el mantenimiento del software;
- permite reutilizar componentes;
- simplifica las pruebas;
- favorece el trabajo colaborativo;
- mejora la escalabilidad del sistema.

En los próximos apartados aprenderemos cómo se organizan estos componentes y cómo integrarlos con CoppeliaSim.

## 23.2 Los nodos: los bloques fundamentales de ROS 2

La idea principal de ROS 2 consiste en dividir una aplicación robótica en pequeños programas independientes.

Cada uno de estos programas recibe el nombre de **nodo** (*Node*).

Un nodo realiza una única tarea y la realiza bien.

Por ejemplo, en una aplicación industrial podríamos encontrar los siguientes nodos:

- un nodo que controla el robot UR3;
- un nodo encargado de adquirir imágenes desde una cámara;
- un nodo que detecta piezas mediante visión artificial;
- un nodo que calcula trayectorias;
- un nodo que registra información en una base de datos;
- un nodo que muestra el estado del sistema en un panel de supervisión.

Todos ellos funcionan de forma simultánea y colaboran para conseguir un objetivo común.

La siguiente figura representa esta organización.

::: figure
image: ../assets/cap23/fig23_2.png
caption: Un sistema robótico dividido en varios nodos independientes.
:::

Observa que cada nodo tiene una responsabilidad concreta.

Esta filosofía presenta numerosas ventajas.

Si un nodo necesita modificarse, normalmente no será necesario cambiar el resto de la aplicación.

Además, diferentes equipos de desarrollo pueden trabajar de forma paralela sobre distintos nodos.

---

### Un ejemplo cotidiano

Podemos comparar un sistema ROS 2 con el funcionamiento de una empresa.

En una empresa encontramos diferentes departamentos:

- administración;
- recursos humanos;
- compras;
- logística;
- producción.

Cada departamento realiza un trabajo específico.

Sin embargo, todos colaboran para alcanzar un objetivo común.

En ROS 2 ocurre exactamente lo mismo.

Cada nodo desempeña una función concreta y se comunica con los demás cuando necesita intercambiar información.

::: teacher
content:

Muchos alumnos entienden mejor el concepto de nodo cuando se compara con departamentos de una empresa o con aplicaciones independientes abiertas simultáneamente en un ordenador.

El objetivo es que comprendan que un nodo no es una función ni una clase, sino un programa completo con una responsabilidad bien definida.
:::

---

## 23.3 ¿Cómo se comunican los nodos?

Si cada nodo trabaja de forma independiente, surge una pregunta evidente:

**¿Cómo intercambian información?**

ROS 2 resuelve este problema mediante diferentes mecanismos de comunicación.

El más utilizado recibe el nombre de **topic**.

Un topic puede imaginarse como un canal de comunicación.

Un nodo publica información en ese canal y cualquier otro nodo interesado puede recibirla.

El nodo que envía la información recibe el nombre de **publicador** (*Publisher*).

El nodo que la recibe se denomina **suscriptor** (*Subscriber*).

La siguiente figura muestra este mecanismo.

::: figure
image: ../assets/cap23/fig23_3.png
caption: Comunicación mediante topics entre nodos ROS 2.
:::

Gracias a este sistema, los nodos no necesitan conocerse entre sí.

Únicamente necesitan conocer el nombre del topic por el que desean comunicarse.

Esta característica convierte a ROS 2 en una plataforma muy flexible y escalable.

---

### Un ejemplo práctico

Imaginemos una célula robotizada compuesta por un robot UR3 y una cámara de visión.

El nodo encargado de la cámara detecta continuamente la posición de las piezas.

Cada vez que obtiene una nueva medida, publica las coordenadas en un topic llamado:

```text
/piezas
```

El nodo encargado del control del robot está suscrito a ese topic.

Cada vez que recibe unas nuevas coordenadas, calcula automáticamente el movimiento que debe realizar el UR3 para recoger la pieza.

Observa que ninguno de los dos nodos conoce cómo está implementado el otro.

Únicamente intercambian información mediante el topic compartido.

Este desacoplamiento constituye una de las principales ventajas de ROS 2.

::: common-error
content:

Es habitual pensar que un nodo envía mensajes directamente a otro nodo.

En realidad, los mensajes se publican en un topic y cualquier nodo suscrito a ese topic puede recibirlos.

Los nodos no se comunican directamente entre sí.
:::

---

## Ventajas de una arquitectura basada en nodos

Dividir una aplicación en varios nodos independientes aporta numerosos beneficios.

Entre los más importantes destacan:

- facilita el mantenimiento del software;
- permite reutilizar componentes en diferentes proyectos;
- mejora la tolerancia a fallos;
- simplifica las pruebas;
- favorece el trabajo colaborativo;
- facilita la ampliación de sistemas complejos.

Gracias a estas características, ROS 2 se ha convertido en el estándar utilizado actualmente en investigación, automatización industrial y robótica de servicios.

En el siguiente apartado aprenderemos cómo crear nuestros primeros nodos y cómo ejecutarlos desde la línea de comandos.

## 23.4 Publicadores y suscriptores

En el apartado anterior vimos que los nodos intercambian información mediante **topics**.

Ahora estudiaremos quién envía esa información y quién la recibe.

En ROS 2 existen dos elementos fundamentales:

- **Publicador (Publisher)**: nodo que envía información a un topic.
- **Suscriptor (Subscriber)**: nodo que recibe la información publicada en ese topic.

Este modelo de comunicación resulta muy eficiente porque desacopla completamente los diferentes componentes de la aplicación.

Un publicador no necesita conocer qué nodos recibirán sus mensajes.

De igual forma, un suscriptor tampoco necesita saber quién genera la información.

Ambos únicamente deben conocer el nombre del topic.

La siguiente figura resume este mecanismo.

::: figure
image: ../assets/cap23/fig23_4.png
caption: Comunicación entre un publicador y uno o varios suscriptores mediante un topic.
:::

---

### Un ejemplo en una célula robotizada

Supongamos una célula de clasificación automática equipada con un robot **UR3** y una cámara de visión artificial.

El funcionamiento podría ser el siguiente:

1. La cámara detecta una pieza sobre la cinta transportadora.
2. El nodo de visión calcula sus coordenadas.
3. El nodo publica esa información en el topic `/pieza_detectada`.
4. El nodo de control del UR3 recibe las coordenadas.
5. El robot planifica el movimiento y recoge la pieza.

En ningún momento el nodo de visión necesita conocer cómo funciona el robot.

Simplemente publica los datos en el topic correspondiente.

Este diseño facilita enormemente el desarrollo y mantenimiento de aplicaciones complejas.

::: teacher
content:

Un buen ejercicio consiste en pedir al alumnado que identifique qué nodos actuarían como publicadores y cuáles como suscriptores en diferentes aplicaciones robóticas.

Este análisis ayuda a comprender la arquitectura distribuida de ROS 2 antes de comenzar a programar.
:::

---

## 23.5 Los servicios

No toda la comunicación en ROS 2 consiste en publicar información continuamente.

En muchas ocasiones un nodo necesita solicitar una operación concreta y esperar una respuesta.

Para estos casos ROS 2 incorpora los **servicios** (*Services*).

Un servicio funciona de manera muy similar a una llamada a una función.

Un nodo realiza una petición.

Otro nodo procesa la solicitud.

Finalmente devuelve una respuesta.

La siguiente figura representa este mecanismo.

::: figure
image: ../assets/cap23/fig23_5.png
caption: Comunicación mediante un servicio en ROS 2.
:::

---

### Diferencias entre un topic y un servicio

Aunque ambos mecanismos permiten comunicar nodos, cada uno está pensado para un tipo de aplicación diferente.

::: table
caption: Comparación entre topics y servicios.
content:

| Característica | Topic | Servicio |
|----------------|-------|----------|
| Comunicación | Continua | Bajo demanda |
| Respuesta | No obligatoria | Siempre existe una respuesta |
| Número de receptores | Uno o varios | Normalmente uno |
| Uso habitual | Sensores, cámaras, estado del robot | Solicitudes puntuales |

:::

Como regla general:

- utilizaremos **topics** cuando sea necesario intercambiar información de forma continua;
- utilizaremos **servicios** cuando un nodo necesite realizar una petición concreta.

---

### Ejemplo práctico

Imaginemos que una aplicación necesita conocer la posición actual del robot UR3.

Existen dos posibilidades.

**Mediante un topic**

El nodo del robot publica continuamente su posición.

Cualquier nodo interesado puede leer esa información en cualquier momento.

**Mediante un servicio**

El nodo cliente solicita la posición únicamente cuando la necesita.

El nodo servidor responde con las coordenadas actuales del robot.

Elegir uno u otro mecanismo dependerá del tipo de información que queramos intercambiar.

::: common-error
content:

No todos los problemas deben resolverse utilizando topics.

Un error frecuente consiste en publicar información continuamente cuando bastaría con realizar una única petición mediante un servicio.

Elegir correctamente el mecanismo de comunicación mejora el rendimiento y simplifica el diseño de la aplicación.
:::

---

## Preparando nuestro primer nodo ROS 2

Ya conocemos los principales mecanismos de comunicación utilizados por ROS 2.

En el siguiente apartado crearemos nuestro primer nodo y aprenderemos a ejecutarlo desde la línea de comandos.

A partir de ese momento comenzaremos a integrar ROS 2 con CoppeliaSim y desarrollaremos nuestras primeras aplicaciones distribuidas utilizando el robot **UR3** como plataforma de referencia.

## 23.6 Preparando el entorno de trabajo

Después de comprender cómo se comunican los nodos mediante **topics** y **servicios**, ha llegado el momento de preparar el entorno de desarrollo.

En este capítulo trabajaremos con cuatro herramientas principales:

- **CoppeliaSim EDU 4.10** como simulador.
- **ROS 2** como plataforma de comunicación.
- **Python** como lenguaje de programación.
- **Visual Studio Code** como entorno de desarrollo.

Cada una de ellas desempeña una función específica dentro de la arquitectura que construiremos durante esta parte del libro.

La siguiente figura muestra la relación entre todos estos componentes.

::: figure
image: ../assets/cap23/fig23_6.png
caption: Entorno de desarrollo utilizado para integrar ROS 2 con CoppeliaSim.
:::

---

### El papel de cada herramienta

Aunque todas forman parte del mismo sistema, sus responsabilidades son diferentes.

**CoppeliaSim**

Será el encargado de simular el entorno robótico.

En él ejecutaremos las escenas, simularemos sensores y controlaremos el robot **UR3**.

**ROS 2**

Actuará como la infraestructura de comunicación.

Todos los nodos intercambiarán información utilizando los mecanismos proporcionados por ROS 2.

**Python**

Será el lenguaje utilizado para desarrollar nuestros nodos.

Elegimos Python porque ya lo conocemos de capítulos anteriores y permite centrarse en la lógica de programación sin añadir complejidad innecesaria.

**Visual Studio Code**

Lo utilizaremos para escribir, ejecutar y depurar nuestros programas.

---

## Instalando ROS 2

ROS 2 puede instalarse en diferentes sistemas operativos.

Actualmente existen distribuciones para:

- Ubuntu (la plataforma oficial).
- Windows.
- macOS.

En este libro utilizaremos **ROS 2 Jazzy Jalisco**, ya que es una versión con soporte a largo plazo (LTS) y totalmente compatible con las versiones actuales de CoppeliaSim.

La instalación completa puede consultarse en la documentación oficial de ROS 2.

No obstante, en las prácticas del libro partiremos siempre de un entorno ya preparado para evitar dedicar demasiado tiempo a tareas de configuración.

::: teacher
content:

Si el aula dispone de varios equipos, es recomendable instalar previamente ROS 2 en todos ellos y comprobar que el entorno está correctamente configurado.

De esta forma la sesión podrá centrarse en la programación y no en la resolución de incidencias de instalación.
:::

---

## 23.7 El espacio de trabajo (*Workspace*)

Todos los proyectos ROS 2 se organizan dentro de un directorio denominado **workspace**.

Podemos imaginarlo como la carpeta principal de un proyecto.

En ella almacenaremos:

- los paquetes ROS 2;
- los nodos desarrollados en Python;
- los archivos de configuración;
- los recursos utilizados por la aplicación.

Una organización adecuada facilitará el mantenimiento de nuestros proyectos conforme vayan aumentando de tamaño.

La siguiente figura representa la estructura básica de un workspace.

::: figure
image: ../assets/cap23/fig23_7.png
caption: Organización de un workspace en ROS 2.
:::

---

### Estructura recomendada

Aunque ROS 2 permite diferentes organizaciones, utilizaremos la siguiente estructura durante todo el libro.

```text
ros2_ws/
│
├── src/
│   └── robot_ur3/
│       ├── package.xml
│       ├── setup.py
│       ├── robot_ur3/
│       │   ├── __init__.py
│       │   └── nodo_control.py
│       └── resource/
│
├── build/
├── install/
└── log/
```

No es necesario memorizar todos estos directorios.

Muchos de ellos serán creados automáticamente por las herramientas de ROS 2.

Conforme avancemos en el capítulo aprenderemos qué función desempeña cada uno.

::: common-error
content:

Un error muy habitual consiste en crear los archivos Python fuera del directorio `src`.

ROS 2 únicamente localizará correctamente los paquetes que se encuentren dentro del workspace siguiendo la estructura establecida.
:::

---

### Preparando nuestro primer nodo

Ya tenemos todo preparado para comenzar a programar.

En el siguiente apartado crearemos nuestro primer nodo ROS 2 utilizando Python, lo ejecutaremos desde la terminal y comprobaremos que el sistema es capaz de iniciar correctamente un nodo dentro del workspace.

Este será el punto de partida para integrar posteriormente ROS 2 con CoppeliaSim y controlar el robot **UR3** mediante una arquitectura distribuida.

## 23.8 Nuestro primer nodo ROS 2

Ya tenemos preparado el entorno de trabajo.

Ha llegado el momento de crear nuestro primer nodo utilizando Python.

El objetivo de este ejemplo no será controlar todavía el robot UR3.

Simplemente comprobaremos que somos capaces de crear y ejecutar un nodo dentro de ROS 2.

### Creando el nodo

Dentro del paquete `robot_ur3` crea un archivo llamado:

```text
primer_nodo.py
```

A continuación escribe el siguiente programa.

```python
import rclpy
from rclpy.node import Node


class PrimerNodo(Node):

    def __init__(self):
        super().__init__('primer_nodo')
        self.get_logger().info('¡Hola desde ROS 2!')


def main(args=None):
    rclpy.init(args=args)

    nodo = PrimerNodo()

    rclpy.spin_once(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Aunque el programa es muy sencillo, incorpora todos los elementos básicos que tendrá cualquier aplicación desarrollada con ROS 2.

Cuando lo ejecutemos, aparecerá un mensaje similar al siguiente:

```text
[INFO] [primer_nodo]: ¡Hola desde ROS 2!
```

Este mensaje confirma que el nodo se ha creado correctamente y que ROS 2 está funcionando.

---

## Analizando el código

Veamos qué realiza cada una de las partes del programa.

```python
import rclpy
```

Importa la biblioteca principal de ROS 2 para Python.

---

```python
from rclpy.node import Node
```

Importa la clase base que utilizarán todos nuestros nodos.

---

```python
class PrimerNodo(Node):
```

Define un nuevo nodo llamado `PrimerNodo`.

Todas las aplicaciones ROS 2 se construyen creando clases que heredan de `Node`.

---

```python
super().__init__('primer_nodo')
```

Asigna el nombre del nodo dentro de la red ROS 2.

Este nombre permitirá identificarlo cuando existan varios nodos ejecutándose simultáneamente.

---

```python
self.get_logger().info(...)
```

Envía un mensaje a la consola utilizando el sistema de registro (*logging*) de ROS 2.

Este mecanismo resulta mucho más potente que utilizar simplemente la función `print()`.

::: teacher
content:

Acostumbra al alumnado a utilizar el sistema de registro de ROS 2 desde el principio.

Más adelante facilitará enormemente la depuración de aplicaciones distribuidas con numerosos nodos ejecutándose simultáneamente.
:::

---

## Ejecutando el nodo

Una vez compilado el workspace podremos ejecutar nuestro nodo utilizando el siguiente comando.

```bash
ros2 run robot_ur3 primer_nodo
```

Si todo funciona correctamente aparecerá el mensaje mostrado anteriormente.

Con este sencillo ejemplo ya hemos conseguido ejecutar nuestro primer nodo ROS 2.

En los siguientes capítulos añadiremos publicadores, suscriptores y servicios para comenzar a intercambiar información con CoppeliaSim y controlar el robot UR3.

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Nodo | Programa independiente que realiza una tarea concreta dentro de ROS 2. |
| Topic | Canal de comunicación utilizado por los nodos para intercambiar mensajes. |
| Publisher | Nodo que publica información en un topic. |
| Subscriber | Nodo que recibe información de un topic. |
| Servicio | Comunicación basada en petición y respuesta. |
| Workspace | Directorio donde se organizan los proyectos ROS 2. |
| Paquete | Unidad básica de organización del código en ROS 2. |
| rclpy | Biblioteca oficial de ROS 2 para Python. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender la arquitectura distribuida de ROS 2.
- ✅ Explicar qué son los nodos y los topics.
- ✅ Diferenciar entre publicadores, suscriptores y servicios.
- ✅ Preparar un workspace para desarrollar aplicaciones ROS 2.
- ✅ Crear y ejecutar un primer nodo utilizando Python.
- ✅ Comprender cómo se integrará ROS 2 con CoppeliaSim.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué es un nodo en ROS 2?
2. ¿Cuál es la función de un topic?
3. ¿Qué diferencia existe entre un publicador y un suscriptor?
4. ¿En qué situaciones resulta más adecuado utilizar un servicio?
5. ¿Qué contiene un workspace?
6. ¿Qué función desempeña la biblioteca `rclpy`?
7. ¿Qué comando permite ejecutar un nodo desde la terminal?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a desarrollar aplicaciones distribuidas con ROS 2.

---

## Práctica guiada

::: practice
title: Creando el primer nodo ROS 2

difficulty: Media

time: 45 minutos

content:

Realiza las siguientes tareas.

1. Abre el workspace creado anteriormente.
2. Comprueba que el entorno ROS 2 está correctamente configurado.
3. Crea el archivo `primer_nodo.py`.
4. Escribe el código mostrado en este capítulo.
5. Compila el workspace.
6. Ejecuta el nodo desde la terminal.
7. Comprueba que aparece el mensaje de bienvenida.
8. Modifica el nombre del nodo y vuelve a ejecutarlo.
9. Cambia el mensaje mostrado por consola.
10. Analiza el resultado obtenido.

El objetivo de la práctica es comprender el ciclo de vida básico de un nodo ROS 2.

:::

---

## Reto

::: challenge
title: Explorando el ecosistema ROS 2

content:

Investiga qué otros comandos proporciona la utilidad `ros2`.

Intenta localizar:

- los nodos activos;
- los topics disponibles;
- los servicios registrados.

Aunque todavía no conozcas su funcionamiento, familiarizarte con estas herramientas facilitará enormemente el aprendizaje de los próximos capítulos.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender la filosofía de ROS 2.
- Crear el primer nodo utilizando Python.
- Familiarizar al alumnado con la estructura de un workspace.
- Ejecutar un nodo desde la terminal.

**Material necesario**

- ROS 2 Jazzy instalado.
- CoppeliaSim EDU 4.10.
- Visual Studio Code.
- Python 3.x.

**Consejos metodológicos**

No intentes explicar todas las posibilidades de ROS 2 en este capítulo.

El objetivo consiste únicamente en que el alumnado comprenda la arquitectura distribuida y sea capaz de ejecutar su primer nodo.

La comunicación con CoppeliaSim comenzará en el siguiente capítulo.

:::

---

## Próximo capítulo

Ya sabemos crear nodos ROS 2.

En el siguiente capítulo aprenderemos a comunicar CoppeliaSim con el exterior utilizando protocolos industriales como **OPC UA**, **MQTT**, **TCP/IP** y **REST API**.

Estos mecanismos permitirán integrar el simulador con PLC, bases de datos, paneles de supervisión y otras aplicaciones industriales, acercándonos a los sistemas utilizados actualmente en la Industria 4.0.