::: chapter-cover
number: 7
title: Robots móviles: primeros pasos
time: 4 horas
level: ⭐⭐☆☆☆ (Inicial)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Identificar las características principales de un robot móvil.
- Conocer la estructura del Pioneer P3DX.
- Incorporar un robot móvil a una escena.
- Comprender la función de sus sensores y actuadores.
- Manipular manualmente el robot dentro de CoppeliaSim.
- Preparar el robot para ser controlado mediante Python.
:::

# Capítulo 7 · Robots móviles: primeros pasos

### ¿Por qué aprender con un robot móvil?

Hasta ahora hemos aprendido a utilizar CoppeliaSim como entorno de simulación.

Sin embargo, todavía no hemos trabajado con un robot real.

Ha llegado el momento de comenzar.

Durante este capítulo conoceremos el Pioneer P3DX, uno de los robots móviles más utilizados en universidades y centros de investigación.

Aunque inicialmente aprenderemos a moverlo manualmente, muy pronto comenzaremos a controlarlo mediante Python, exactamente igual que haríamos con un robot físico.

Este será el punto de partida para el resto de la parte dedicada a robótica móvil.

::: teacher
content:

No intentes explicar todavía el funcionamiento interno del robot.

En esta primera sesión el objetivo consiste únicamente en que el alumnado se familiarice con la plataforma y pierda el miedo a manipularla dentro de CoppeliaSim.
:::

---

## 7.2 Características del Pioneer P3DX

Como hemos visto, el Pioneer P3DX será el robot protagonista de buena parte de este libro.

Antes de comenzar a programarlo conviene conocer cómo está construido y qué elementos incorpora.

Aunque externamente pueda parecer un robot muy sencillo, en realidad integra todos los componentes habituales de una plataforma móvil utilizada en investigación.

Esto lo convierte en un excelente punto de partida para aprender robótica.

::: figure
image: ../assets/cap07/annotated/pioneer_p3dx.png
caption: Robot móvil Pioneer P3DX en CoppeliaSim.
:::

### Un robot de tracción diferencial

El Pioneer P3DX pertenece a la familia de los **robots de tracción diferencial**.

Su desplazamiento se consigue mediante dos ruedas motrices situadas a ambos lados del chasis.

Cada rueda dispone de su propio motor y puede girar a una velocidad diferente.

La combinación de ambas velocidades permite realizar todos los movimientos del robot.

Por ejemplo:

- si ambas ruedas giran a la misma velocidad, el robot avanza en línea recta;
- si una rueda gira más deprisa que la otra, el robot describe una curva;
- si las ruedas giran en sentidos opuestos, el robot gira prácticamente sobre su propio eje.

Este sistema de locomoción es uno de los más utilizados en robótica educativa y de investigación por su sencillez y precisión.

::: teacher
content:

No es necesario explicar todavía la cinemática diferencial.

En este capítulo basta con que el alumnado comprenda intuitivamente que el movimiento depende de la velocidad de cada rueda.

Los cálculos matemáticos se estudiarán más adelante.
:::

---

### Componentes principales

Aunque veremos el robot con mucho más detalle en capítulos posteriores, es conveniente identificar desde este momento sus elementos más importantes.

::: figure
image: ../assets/cap07/annotated/componentes_pioneer.png
caption: Componentes principales del robot Pioneer P3DX.
:::

El Pioneer P3DX está formado por:

- un chasis que soporta todos los componentes;
- dos ruedas motrices laterales;
- una rueda libre de apoyo;
- varios sensores distribuidos alrededor del robot;
- motores eléctricos para el movimiento;
- una unidad de control encargada de coordinar todos los elementos.

Cada uno de estos componentes cumple una función específica.

Trabajando conjuntamente permiten que el robot pueda desplazarse, detectar obstáculos y reaccionar ante diferentes situaciones.

Más adelante aprenderemos a acceder desde Python a muchos de estos elementos.

---

### El chasis

El chasis constituye la estructura principal del robot.

Sobre él se montan los motores, las ruedas, los sensores y todos los dispositivos electrónicos.

Además de proporcionar rigidez mecánica, sirve como referencia para definir el sistema de coordenadas local del robot.

Cuando movemos el Pioneer P3DX en CoppeliaSim, realmente estamos desplazando su chasis y, con él, todos los componentes que dependen de esta estructura.

---

### Las ruedas motrices

Las dos ruedas laterales son las responsables del desplazamiento.

Cada una puede girar de forma completamente independiente.

Esta independencia es precisamente la que permite realizar maniobras muy precisas.

Por ejemplo, el robot puede:

- avanzar;
- retroceder;
- describir curvas suaves;
- girar sobre sí mismo.

En los próximos capítulos aprenderemos a controlar directamente la velocidad de cada rueda mediante Python.

---

### La rueda de apoyo

Además de las ruedas motrices, el Pioneer incorpora una tercera rueda situada en la parte posterior.

Esta rueda no impulsa el robot.

Su única misión consiste en mantener el equilibrio del conjunto y facilitar el desplazamiento sobre el suelo.

Al girar libremente en cualquier dirección apenas ofrece resistencia al movimiento.

Muchos robots móviles reales utilizan exactamente esta misma configuración.

::: info "¿Por qué solo dos ruedas motrices?"

Podría parecer que cuatro ruedas proporcionarían mayor estabilidad.

Sin embargo, utilizar únicamente dos ruedas motrices y una rueda libre simplifica enormemente el control del robot y reduce el número de motores necesarios.

Por este motivo es una configuración muy habitual tanto en robots educativos como en plataformas profesionales.
:::

---

## 7.3 Sensores incorporados

Un robot sería prácticamente inútil si no pudiera obtener información del entorno que le rodea.

Los sensores actúan como los órganos de percepción del robot.

Gracias a ellos puede detectar obstáculos, medir distancias, localizar objetos o conocer su propia posición.

El Pioneer P3DX incluido en CoppeliaSim incorpora varios sensores ya configurados y completamente funcionales.

Durante este libro utilizaremos principalmente los sensores de proximidad, aunque el simulador permite añadir muchos otros dispositivos.

No estudiaremos todavía su funcionamiento interno.

Por ahora basta con comprender que los sensores proporcionan la información necesaria para que el robot pueda tomar decisiones de forma autónoma.

En los próximos capítulos aprenderemos a leer estos sensores desde Python y utilizarlos para construir comportamientos cada vez más inteligentes.

---

## 7.4 Incorporando el Pioneer P3DX a una escena

Ha llegado el momento de trabajar con nuestro primer robot.

Hasta ahora hemos utilizado escenas de ejemplo y hemos aprendido a movernos por la interfaz de CoppeliaSim.

A partir de este momento comenzaremos a construir nuestras propias simulaciones.

El primer paso consiste en incorporar el robot Pioneer P3DX a una escena vacía.

Como ya aprendimos en el Capítulo 3, CoppeliaSim incluye una extensa biblioteca de modelos preparados para utilizarse directamente.

El Pioneer P3DX forma parte de esa biblioteca.

No tendremos que construir el robot pieza a pieza.

Simplemente lo seleccionaremos y lo arrastraremos hasta la escena.

---

### Crear una escena nueva

Antes de añadir el robot conviene comenzar con una escena completamente vacía.

Para ello:

1. Abre el menú **File**.
2. Selecciona **New Scene**.
3. Guarda la escena con el nombre **capitulo07.ttt**.

Trabajar desde una escena limpia facilita comprender el funcionamiento del robot y evita distracciones provocadas por otros objetos.

::: common-error
content:

Muchos estudiantes comienzan a trabajar sobre una escena de ejemplo descargada de Internet.

Esto suele introducir numerosos objetos, scripts y sensores que dificultan el aprendizaje.

Para las primeras prácticas es recomendable utilizar siempre una escena completamente vacía.
:::

---

### Localizar el robot en la biblioteca

Una vez creada la escena debemos abrir la biblioteca de modelos.

Si el panel **Model Browser** no está visible, podemos mostrarlo desde la interfaz de CoppeliaSim.

Dentro de la biblioteca encontraremos diferentes categorías organizadas por tipo de dispositivo.

El Pioneer P3DX se encuentra dentro de la categoría dedicada a los robots móviles.

Localizar un modelo resulta sencillo gracias a la organización jerárquica de la biblioteca.

A medida que avancemos en el libro utilizaremos muchos otros robots, sensores y dispositivos disponibles en este catálogo.

::: teacher
content:

Aprovecha este momento para que el alumnado explore brevemente la biblioteca.

Es habitual que descubran robots y dispositivos que despertarán su curiosidad y aumentarán su motivación.
:::

---

### Insertar el robot en la escena

Una vez localizado el Pioneer P3DX, basta con arrastrarlo desde la biblioteca hasta la vista tridimensional.

Cuando soltamos el botón del ratón, el robot aparece automáticamente sobre el plano de trabajo.

No es necesario realizar ninguna configuración adicional.

El modelo ya incorpora todos los elementos necesarios para funcionar correctamente.

Entre ellos se encuentran:

- la estructura mecánica;
- las ruedas motrices;
- los sensores;
- los motores;
- los scripts internos de control;
- las propiedades físicas utilizadas por el simulador.

En realidad, el robot que vemos es mucho más complejo de lo que aparenta.

Gran parte de esa complejidad permanece oculta para facilitar su utilización.

---

### El robot aparece también en el árbol de la escena

Después de insertar el Pioneer P3DX observarás que también aparece un nuevo elemento en el árbol de la escena.

Esto confirma que el robot ya forma parte de nuestra simulación.

Si desplegamos dicho elemento descubriremos que está formado por numerosos objetos organizados jerárquicamente.

Encontraremos, entre otros:

- el cuerpo principal del robot;
- las ruedas;
- diferentes sensores;
- scripts internos;
- elementos auxiliares utilizados por la simulación.

Esta organización resulta muy similar a la que tendría un robot físico real.

Cada componente desempeña una función concreta y todos trabajan conjuntamente para formar un único sistema.

No es necesario comprender todavía el significado de cada uno de estos elementos.

En los próximos capítulos iremos estudiándolos poco a poco.

---

### Seleccionar el robot

Existen dos formas principales de seleccionar el Pioneer P3DX.

La primera consiste en hacer clic directamente sobre el robot en la vista tridimensional.

La segunda consiste en seleccionarlo desde el árbol de la escena.

Ambos procedimientos producen exactamente el mismo resultado.

Cuando el robot está seleccionado, CoppeliaSim muestra diferentes indicadores visuales que permiten identificar el objeto activo.

Acostúmbrate desde el principio a comprobar siempre qué objeto tienes seleccionado antes de realizar cualquier modificación.

::: info "Un buen hábito"

En escenas sencillas apenas existen unos pocos objetos.

Sin embargo, en proyectos reales pueden convivir cientos de elementos.

Seleccionar el objeto correcto antes de modificarlo evitará muchos errores durante el desarrollo de las simulaciones.
:::

---

### Guardar la escena

Una vez insertado el robot es recomendable guardar el trabajo.

Aunque parezca un paso evidente, adquirir este hábito desde el principio evitará la pérdida de muchas horas de trabajo.

Durante el desarrollo de este libro modificaremos continuamente nuestras escenas.

Guardar con frecuencia debe convertirse en una costumbre.

En el siguiente apartado comenzaremos a explorar la estructura interna del Pioneer P3DX para comprender cómo está organizado y qué función desempeña cada uno de sus componentes.

---

## 7.5 Anatomía del Pioneer P3DX

A simple vista el Pioneer P3DX parece un único objeto.

Sin embargo, internamente está formado por decenas de elementos organizados de forma jerárquica.

Cada uno de ellos desempeña una función específica dentro de la simulación.

Comprender esta organización resulta muy importante.

Cuando comencemos a programar el robot desde Python necesitaremos acceder a muchos de estos componentes de forma individual.

Por este motivo conviene dedicar unos minutos a explorar su estructura.

---

### Una jerarquía de objetos

Si desplegamos el Pioneer P3DX en el árbol de la escena observaremos que aparecen numerosos elementos.

::: figure
image: ../assets/cap07/annotated/arbol_pioneer_p3d.png
caption: Estructura jerárquica del Pioneer P3DX en el árbol de la escena de CoppeliaSim.
:::

No todos tienen la misma importancia.

Algunos representan componentes físicos visibles, mientras que otros únicamente sirven para organizar la simulación o facilitar el funcionamiento interno del robot.

Esta estructura jerárquica permite agrupar todos los componentes relacionados bajo un único modelo.

Gracias a ello, mover el robot implica desplazar automáticamente todos los elementos que forman parte de él.

Es exactamente el mismo concepto que vimos en el Capítulo 3 al estudiar el árbol de la escena, aunque ahora aplicado a un robot completo.

---

### El cuerpo principal

El elemento principal del modelo corresponde al chasis del robot.

Este componente actúa como referencia para el resto de los objetos.

Cuando desplazamos el Pioneer P3DX por la escena, el movimiento se realiza tomando este elemento como base.

Además, el sistema de coordenadas local del robot se define respecto a este cuerpo principal.

Más adelante utilizaremos esta referencia para conocer la posición y la orientación del robot dentro de la escena.

---

### Las ruedas

El Pioneer dispone de dos ruedas motrices situadas a ambos lados del chasis.

Cada rueda incorpora su propio motor y puede girar de forma independiente.

Esta característica permite controlar con precisión la trayectoria del robot.

En la simulación, las ruedas no son simples elementos gráficos.

Se comportan como articulaciones dinámicas capaces de recibir órdenes de velocidad y transmitir movimiento al robot.

En los próximos capítulos aprenderemos a controlar directamente estas articulaciones desde Python.

---

### Los sensores

Al observar el modelo también encontraremos diferentes sensores distribuidos alrededor del robot.

::: figure
image: ../assets/cap07/annotated/sensores_pioneer_p3dx.png
caption: Distribución aproximada de los sensores ultrasónicos del Pioneer P3DX.
:::

Estos dispositivos permiten detectar información del entorno.

Por ejemplo, podrán indicar la presencia de un obstáculo situado delante del robot o medir la distancia hasta un objeto próximo.

Aunque todavía no utilizaremos estos sensores, es importante saber que ya forman parte del modelo.

No será necesario añadirlos manualmente.

Simplemente aprenderemos a leer la información que proporcionan.

::: info "Un robot preparado para crecer"

El Pioneer P3DX incluido en CoppeliaSim incorpora muchos más elementos de los que utilizaremos en los primeros capítulos.

A medida que aumente la complejidad de las prácticas iremos descubriendo nuevas posibilidades del modelo sin necesidad de sustituir el robot por otro diferente.
:::

---

### Los scripts internos

Si continúas explorando la jerarquía observarás que también aparecen uno o varios scripts asociados al robot.

Estos scripts forman parte del funcionamiento interno del modelo.

Su misión consiste en gestionar determinados aspectos de la simulación para que el Pioneer se comporte correctamente dentro de CoppeliaSim.

No es recomendable modificar estos scripts durante las primeras prácticas.

Nuestro objetivo será controlar el robot desde programas Python externos utilizando la API remota.

De esta forma mantendremos separados el modelo de simulación y nuestro código.

Esta forma de trabajar resulta mucho más profesional y facilita enormemente el mantenimiento de los proyectos.

::: common-error
content:

Algunos estudiantes intentan modificar directamente los scripts internos del Pioneer para cambiar su comportamiento.

Durante este libro no seguiremos ese enfoque.

Todas las prácticas se desarrollarán utilizando programas Python externos que se comunicarán con CoppeliaSim mediante la API remota.
:::

---

### Inspeccionando las propiedades del robot

CoppeliaSim permite consultar las propiedades de cualquier objeto de la escena.

Si seleccionas el Pioneer P3DX y abres su panel de propiedades podrás acceder a información como:

- nombre del objeto;
- posición;
- orientación;
- tamaño;
- propiedades físicas;
- parámetros dinámicos.

No es necesario comprender todavía el significado de todas estas opciones.

En los próximos capítulos trabajaremos principalmente con la posición y la orientación del robot, ya que serán los datos que utilizaremos con mayor frecuencia desde Python.

Dedica unos minutos a explorar este panel.

Cuanto antes te familiarices con él, más cómodo te resultará trabajar cuando las simulaciones sean más complejas.

---

---

## 7.6 Manipulación manual del robot

Antes de comenzar a programar un robot es importante aprender a manipularlo manualmente.

Esto nos permitirá comprender cómo responde dentro de la simulación y nos ayudará a interpretar posteriormente el comportamiento de nuestros programas.

Durante este apartado no escribiremos ninguna línea de código.

Simplemente utilizaremos las herramientas de CoppeliaSim para cambiar la posición y la orientación del Pioneer P3DX.

---

### Seleccionar el robot

El primer paso consiste en seleccionar correctamente el robot.

Podemos hacerlo de dos formas:

- haciendo clic directamente sobre el Pioneer P3DX en la vista tridimensional;
- seleccionándolo desde el árbol de la escena.

Cuando el robot está seleccionado aparecerán diferentes indicadores visuales que confirman cuál es el objeto activo.

Antes de realizar cualquier modificación conviene comprobar siempre que el robot continúa seleccionado.

Este sencillo hábito evitará muchos errores cuando trabajemos con escenas que contengan numerosos objetos.

---

### Desplazar el robot

Una vez seleccionado el Pioneer P3DX podemos modificar su posición utilizando la herramienta **Trasladar objeto**.

Al activarla aparecerán unos manipuladores alineados con los ejes del sistema de coordenadas.

Cada uno de ellos permite desplazar el robot únicamente en una dirección.

Por ejemplo:

- el eje **X** permite mover el robot hacia la derecha o hacia la izquierda;
- el eje **Y** permite desplazarlo hacia delante o hacia atrás;
- el eje **Z** permite elevarlo o bajarlo respecto al suelo.

Durante la mayor parte del libro únicamente modificaremos la posición sobre el plano de trabajo.

En consecuencia, los movimientos se realizarán principalmente sobre los ejes **X** e **Y**.

::: figure
image: ../assets/cap07/annotated/manipulacion_manual.png
caption: Manipulación manual del Pioneer P3DX mediante la herramienta de traslación.
:::

::: common-error
content:

Evita elevar el robot sobre el eje **Z** durante las primeras prácticas.

Si el Pioneer queda suspendido en el aire, la simulación puede comenzar con una caída provocada por la gravedad, dando la impresión de que existe algún error en el programa.
:::

---

### Cambiar la orientación

Además de modificar su posición, también podemos cambiar la orientación del robot.

::: figure
image: ../assets/cap07/svg/rotacion_manual_pioneer.svg
caption: Rotación manual del Pioneer P3DX sobre el eje Z.
:::

Para ello utilizaremos la herramienta **Rotar objeto**.

Al activarla aparecerán unos anillos de colores que representan los diferentes ejes de rotación.

Girando el robot sobre el eje vertical conseguiremos que mire hacia una dirección diferente.

Este movimiento será especialmente importante cuando comencemos a desarrollar algoritmos de navegación.

Un mismo punto de la escena puede alcanzarse con orientaciones completamente distintas.

Por este motivo debemos acostumbrarnos desde el principio a diferenciar claramente entre **posición** y **orientación**.

---

### Posicionar correctamente el Pioneer

En muchas ocasiones necesitaremos colocar el robot en una posición muy concreta.

Por ejemplo, al comenzar una práctica todos los estudiantes deberían partir exactamente desde el mismo lugar.

Para conseguirlo podemos utilizar dos procedimientos diferentes.

El primero consiste en mover el robot manualmente utilizando los manipuladores.

El segundo consiste en introducir directamente las coordenadas desde el panel de propiedades.

Ambos métodos producen el mismo resultado.

Sin embargo, cuando sea necesario repetir exactamente una práctica, resulta mucho más preciso introducir los valores numéricos.

En el Capítulo 5 aprendimos a trabajar con las coordenadas de los objetos.

Ahora comenzamos a aplicar esos conocimientos sobre un robot completo.

::: teacher
content:

Pide al alumnado que coloque todos los robots exactamente en la misma posición antes de comenzar los ejercicios.

Esto facilitará enormemente el seguimiento de las prácticas y permitirá comparar los resultados obtenidos por toda la clase.
:::

---

### Probar la simulación

Una vez colocado el Pioneer P3DX podemos iniciar la simulación pulsando el botón **Play**.

En esta primera práctica probablemente el robot permanecerá inmóvil.

Esto es completamente normal.

Aunque el modelo incorpora motores y sensores, todavía no hemos enviado ninguna orden que produzca movimiento.

Nuestro objetivo en este momento consiste únicamente en comprobar que:

- el robot está correctamente insertado en la escena;
- la simulación se inicia sin errores;
- el Pioneer permanece estable sobre el suelo;
- la escena puede iniciarse y detenerse correctamente.

Si todo funciona como esperas, significa que el entorno está preparado para comenzar a programar.

---

### Reiniciar la escena

Después de detener la simulación observarás que el Pioneer vuelve automáticamente a la posición inicial.

Este comportamiento ya lo estudiamos en capítulos anteriores.

CoppeliaSim restaura el estado de la escena para que podamos repetir la práctica tantas veces como sea necesario.

Gracias a ello siempre comenzaremos desde las mismas condiciones iniciales.

Este detalle resulta especialmente importante cuando empecemos a desarrollar programas de control.

Si cada ejecución comenzara desde una posición distinta, sería mucho más difícil localizar posibles errores.

::: info "Preparados para programar"

A partir del próximo apartado dejaremos de mover el robot manualmente.

Será Python quien enviará las órdenes de movimiento al Pioneer P3DX.

Comenzaremos con programas muy sencillos y, poco a poco, construiremos aplicaciones capaces de controlar completamente el robot.
:::

---

---

## 7.7 Primeros movimientos mediante Python

Hasta este momento hemos desplazado el Pioneer P3DX manualmente utilizando las herramientas de CoppeliaSim.

Sin embargo, uno de los grandes objetivos de la robótica consiste en conseguir que sea el propio robot quien ejecute las acciones de forma automática.

Para ello necesitaremos escribir programas capaces de comunicarse con el simulador.

En el capítulo anterior aprendimos a establecer una conexión entre Python y CoppeliaSim mediante la API remota ZeroMQ.

Ha llegado el momento de utilizar esa conexión para controlar nuestro primer robot.

::: figure
image: ../assets/cap07/svg/flujo_python_pioneer.svg
caption: Flujo de control del Pioneer P3DX mediante Python y la API remota ZeroMQ.
:::

Aunque los ejemplos que veremos son muy sencillos, representan el punto de partida de todos los proyectos que desarrollaremos durante el resto del libro.

---

### Conectando con el simulador

Antes de enviar cualquier orden debemos establecer la comunicación con CoppeliaSim.

El procedimiento es exactamente el mismo que aprendimos en el capítulo anterior.

Comenzamos importando la biblioteca de la API remota y creando un cliente de comunicación.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')
```

Si CoppeliaSim está abierto y la escena se encuentra cargada, Python podrá comunicarse inmediatamente con el simulador.

A partir de ese momento podremos acceder a cualquiera de los objetos presentes en la escena.

::: common-error
content:

Si el programa produce un error de conexión, comprueba que CoppeliaSim se encuentra abierto antes de ejecutar el script.

También verifica que la escena está correctamente cargada.

La mayoría de los problemas de este apartado se deben simplemente a que el simulador todavía no está en ejecución.
:::

---

### Localizando el Pioneer P3DX

Para controlar un objeto desde Python primero debemos obtener una referencia a dicho objeto.

Esto se consigue mediante la función `getObject()`.

```python
robot = sim.getObject('/PioneerP3DX')
```

La variable `robot` no contiene el robot completo.

En realidad almacena un identificador interno que CoppeliaSim utilizará para saber sobre qué objeto queremos trabajar.

Este identificador será necesario para prácticamente todas las operaciones que realizaremos a partir de ahora.

---

### Consultando la posición del robot

Una vez obtenido el identificador podemos comenzar a consultar información.

Por ejemplo, podemos conocer la posición actual del Pioneer dentro de la escena.

```python
posicion = sim.getObjectPosition(robot)

print(posicion)
```

La salida será similar a la siguiente:

```text
[0.0, 0.0, 0.1388]
```

Estos tres valores representan las coordenadas del robot respecto al sistema de coordenadas global de la escena.

Como ya estudiamos en el Capítulo 5:

- el primer valor corresponde al eje **X**;
- el segundo corresponde al eje **Y**;
- el tercero corresponde al eje **Z**.

Normalmente trabajaremos sobre los dos primeros, ya que el robot se desplaza sobre el suelo.

::: teacher
content:

Pide al alumnado que ejecute el programa varias veces modificando previamente la posición del robot desde CoppeliaSim.

Observar cómo cambian las coordenadas ayuda mucho a comprender la relación entre el entorno gráfico y la información recibida desde Python.
:::

---

### Consultando la orientación

Además de conocer la posición, también podemos averiguar hacia dónde está orientado el robot.

Para ello utilizamos la función `getObjectOrientation()`.

```python
orientacion = sim.getObjectOrientation(robot)

print(orientacion)
```

Obtendremos una lista con tres ángulos expresados en radianes.

Estos valores describen la orientación del Pioneer respecto a los ejes de referencia de la escena.

Aunque todavía no trabajaremos directamente con ellos, conviene familiarizarse con este tipo de información.

Más adelante utilizaremos estos datos para desarrollar algoritmos de navegación y control.

---

### Nuestro primer programa de inspección

Con muy pocas líneas de código ya somos capaces de conocer el estado del robot.

Podemos saber dónde se encuentra y cuál es su orientación dentro de la escena.

Aunque todavía no hemos conseguido moverlo, este paso es mucho más importante de lo que parece.

Antes de controlar cualquier sistema físico es imprescindible ser capaces de obtener información fiable sobre él.

En robótica se suele decir que **un robot primero observa y después actúa**.

En el siguiente apartado comenzaremos precisamente esa segunda fase.

Será el momento de enviar nuestras primeras órdenes de movimiento al Pioneer P3DX.

---

---

### Enviando nuestro primer movimiento

Hasta ahora nuestro programa únicamente era capaz de obtener información sobre el robot.

Ha llegado el momento de dar el siguiente paso.

Vamos a modificar su posición directamente desde Python.

Para ello utilizaremos la función `setObjectPosition()`.

Su misión consiste en cambiar las coordenadas de un objeto dentro de la escena.

La sintaxis general es la siguiente:

```python
sim.setObjectPosition(objeto, referencia, posicion)
```

Donde:

- **objeto** es el elemento que queremos mover;
- **referencia** indica respecto a qué sistema de coordenadas realizaremos el movimiento;
- **posición** es una lista con las nuevas coordenadas **X**, **Y** y **Z**.

En la mayoría de las primeras prácticas utilizaremos el sistema de coordenadas global.

---

### Cambiando la posición del Pioneer

El siguiente programa desplaza el robot hasta una nueva posición dentro de la escena.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

robot = sim.getObject('/PioneerP3DX')

sim.setObjectPosition(robot, -1, [1.5, 0.0, 0.1388])
```

Al ejecutar el programa observarás que el Pioneer aparece inmediatamente en la nueva posición.

No veremos un desplazamiento continuo.

El robot simplemente cambia de lugar.

Esto ocurre porque estamos modificando directamente sus coordenadas.

Todavía no estamos utilizando los motores del robot.

::: info
content:

Mover un objeto modificando directamente su posición resulta muy útil durante el desarrollo y la depuración de programas.

Sin embargo, un robot real no puede teletransportarse.

Más adelante aprenderemos a desplazar el Pioneer controlando la velocidad de sus ruedas para conseguir movimientos completamente realistas.
:::

---

### ¿Qué significa el valor **-1**?

Probablemente el segundo parámetro de la función haya llamado tu atención.

```python
-1
```

Este valor indica que la nueva posición se expresa respecto al **sistema de coordenadas global** de la escena.

Es decir, las coordenadas hacen referencia al origen general de CoppeliaSim.

Más adelante aprenderemos que también es posible mover un objeto utilizando como referencia otro objeto de la escena.

Por ejemplo:

- otro robot;
- una cámara;
- un sensor;
- una cinta transportadora.

Esta posibilidad resulta muy útil en proyectos complejos.

Por el momento trabajaremos siempre respecto al sistema global.

---

### Desplazamientos sucesivos

Podemos modificar la posición del robot tantas veces como deseemos.

Por ejemplo:

```python
sim.setObjectPosition(robot, -1, [0.0, 0.0, 0.1388])
sim.setObjectPosition(robot, -1, [1.0, 0.0, 0.1388])
sim.setObjectPosition(robot, -1, [2.0, 0.0, 0.1388])
```

Si ejecutamos estas instrucciones consecutivamente, únicamente veremos la última posición.

Python ejecuta las órdenes tan rápidamente que el ojo humano no llega a apreciar los cambios intermedios.

Más adelante aprenderemos a introducir pausas entre los movimientos para observar cómo el robot cambia progresivamente de posición.

---

### Manteniendo la altura correcta

En todos los ejemplos anteriores hemos utilizado siempre el mismo valor para el eje **Z**.

```python
0.1388
```

Este valor corresponde aproximadamente a la altura del Pioneer respecto al plano de trabajo.

Modificar accidentalmente esta coordenada puede producir resultados inesperados.

Por ejemplo:

- el robot puede aparecer flotando;
- puede quedar parcialmente enterrado en el suelo;
- incluso puede caer debido a la acción de la gravedad cuando se inicia la simulación.

Siempre que únicamente quieras desplazar el robot sobre el suelo, modifica únicamente las coordenadas **X** e **Y**.

::: common-error
content:

Uno de los errores más frecuentes consiste en escribir accidentalmente un valor incorrecto para el eje **Z**.

Si el Pioneer desaparece de la escena o parece comportarse de forma extraña, comprueba primero este valor antes de buscar otros posibles errores.
:::

---

### Comprobando el resultado

Después de ejecutar el programa vuelve a consultar la posición del robot utilizando `getObjectPosition()`.

Comprobarás que las coordenadas obtenidas coinciden exactamente con las que acabamos de establecer.

Este sencillo experimento demuestra que Python puede modificar directamente el estado de la simulación.

A partir de este momento ya disponemos de todas las herramientas necesarias para comenzar a controlar el Pioneer P3DX desde nuestros propios programas.

En los próximos capítulos dejaremos de mover el robot cambiando directamente sus coordenadas y aprenderemos a hacerlo utilizando sus motores, exactamente igual que ocurriría en un robot físico.

---

---

## 7.8 Preparando el robot para los próximos capítulos

En este capítulo hemos conocido el Pioneer P3DX y hemos realizado las primeras pruebas de control mediante Python.

Aunque los ejemplos desarrollados hasta ahora son muy sencillos, constituyen la base sobre la que construiremos aplicaciones mucho más complejas.

En los siguientes capítulos aprenderemos a controlar el robot utilizando la velocidad de sus ruedas, interpretar la información proporcionada por sus sensores y desarrollar algoritmos capaces de tomar decisiones de forma autónoma.

Todo ello partirá de los conceptos que acabamos de estudiar.

---

### Una forma diferente de entender la programación

Hasta ahora la mayoría de los programas que hemos desarrollado en Python producían un resultado inmediato en la pantalla.

Por ejemplo:

- mostraban un mensaje;
- realizaban un cálculo;
- procesaban una lista de datos;
- generaban un archivo.

Cuando trabajamos con robótica la situación cambia completamente.

Nuestro programa ya no interactúa únicamente con el ordenador.

Ahora controla un robot que existe dentro de un entorno de simulación.

Cada instrucción puede modificar el comportamiento del Pioneer P3DX y provocar que el robot cambie de posición, detecte un obstáculo o interactúe con otros elementos de la escena.

Esta forma de programar resulta mucho más visual y permite comprobar inmediatamente el efecto de cada línea de código.

---

### La importancia de experimentar

No tengas miedo de modificar los ejemplos propuestos.

Prueba a cambiar las coordenadas del robot.

Muévelo a diferentes posiciones.

Consulta continuamente su orientación.

Experimenta con distintos valores y observa cuidadosamente cómo responde la simulación.

La robótica se aprende, sobre todo, experimentando.

Cuanto más tiempo dediques a probar diferentes situaciones, más fácil te resultará comprender el comportamiento del robot cuando los programas comiencen a ser más complejos.

::: teacher
content:

Anima al alumnado a experimentar libremente con los programas.

Es preferible que descubran el efecto de modificar una coordenada por sí mismos antes que limitarse a copiar el código proporcionado.

La experimentación favorece un aprendizaje mucho más significativo.
:::

---

### Buenas prácticas desde el primer día

Aunque nuestros programas todavía son muy pequeños, conviene adquirir desde el principio algunos hábitos de trabajo.

Procura seguir siempre estas recomendaciones:

- utiliza nombres descriptivos para las variables;
- comenta únicamente aquello que realmente necesite explicación;
- guarda cada práctica en un archivo independiente;
- comprueba que CoppeliaSim está ejecutándose antes de iniciar el programa;
- guarda la escena cada vez que completes una práctica.

Estos pequeños hábitos marcarán una gran diferencia cuando los proyectos comiencen a crecer.

---

### Mirando hacia el futuro

Durante este capítulo hemos movido el Pioneer modificando directamente su posición dentro de la escena.

Este procedimiento resulta muy útil para comprender el funcionamiento de la API remota, pero no representa el comportamiento real de un robot móvil.

En un robot físico no indicamos continuamente sus coordenadas.

Lo que hacemos es controlar la velocidad de los motores que accionan las ruedas.

Será precisamente eso lo que aprenderemos en los próximos capítulos.

A partir de ese momento el Pioneer dejará de "aparecer" en diferentes posiciones y comenzará a desplazarse de forma completamente natural, igual que lo haría un robot real.

::: info "Lo que viene a continuación"

En el siguiente capítulo comenzaremos a trabajar con los sensores del Pioneer P3DX.

Aprenderemos cómo detectar obstáculos, medir distancias e interpretar la información del entorno para que el robot pueda tomar decisiones durante la simulación.
:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Robot móvil | Robot capaz de desplazarse de forma autónoma o controlada dentro de un entorno. |
| Pioneer P3DX | Plataforma robótica móvil utilizada durante buena parte del libro. |
| Tracción diferencial | Sistema de locomoción basado en dos ruedas motrices independientes. |
| Chasis | Estructura principal del robot sobre la que se montan el resto de componentes. |
| Sensor | Dispositivo que permite al robot obtener información del entorno. |
| Actuador | Elemento encargado de producir movimiento o realizar una acción física. |
| API remota | Biblioteca que permite controlar CoppeliaSim desde un programa externo. |
| RemoteAPIClient | Cliente Python utilizado para comunicarse con CoppeliaSim mediante ZeroMQ. |
| getObject() | Función utilizada para obtener la referencia a un objeto de la escena. |
| getObjectPosition() | Permite consultar la posición de un objeto dentro de la simulación. |
| setObjectPosition() | Permite modificar la posición de un objeto desde Python. |
| Sistema de coordenadas global | Sistema de referencia utilizado para posicionar objetos en la escena. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender qué es un robot móvil y cuáles son sus principales componentes.
- ✅ Identificar la estructura general del Pioneer P3DX.
- ✅ Incorporar el robot a una escena de CoppeliaSim.
- ✅ Explorar su organización dentro del árbol de la escena.
- ✅ Manipular manualmente el robot utilizando las herramientas del simulador.
- ✅ Obtener la referencia del Pioneer P3DX desde Python.
- ✅ Consultar su posición y orientación mediante la API remota.
- ✅ Modificar su posición utilizando programas escritos en Python.

A partir de este momento ya estás preparado para comenzar a controlar el robot mediante programación.

En los siguientes capítulos aprenderás a utilizar sus sensores y a desarrollar algoritmos de navegación.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre un robot móvil y un brazo robótico industrial?
2. ¿Qué ventajas ofrece el Pioneer P3DX para el aprendizaje de la robótica?
3. ¿Qué función desempeñan las ruedas motrices en un robot de tracción diferencial?
4. ¿Qué información proporciona la función `getObjectPosition()`?
5. ¿Para qué sirve la función `getObject()`?
6. ¿Qué diferencia existe entre modificar la posición de un robot y controlar directamente sus motores?
7. ¿Por qué es recomendable utilizar Python externo en lugar de modificar los scripts internos del Pioneer P3DX?

Si puedes responder correctamente a todas ellas, estás preparado para continuar.

---

## Práctica guiada

::: practice
title: Primer contacto con el Pioneer P3DX

difficulty: Baja

time: 40 minutos

content:

Realiza las siguientes actividades utilizando una escena nueva de CoppeliaSim.

1. Crea una escena vacía.
2. Inserta el robot Pioneer P3DX desde la biblioteca de modelos.
3. Comprueba que aparece correctamente en el árbol de la escena.
4. Selecciona el robot desde la vista tridimensional y desde el árbol de la escena.
5. Modifica manualmente su posición utilizando la herramienta de traslación.
6. Cambia su orientación utilizando la herramienta de rotación.
7. Guarda la escena.
8. Crea un programa Python que obtenga la referencia del Pioneer mediante `getObject()`.
9. Consulta su posición utilizando `getObjectPosition()`.
10. Modifica su posición mediante `setObjectPosition()` y verifica el resultado dentro de CoppeliaSim.

El objetivo de esta práctica consiste en familiarizarse con el Pioneer P3DX y comprobar que la comunicación entre Python y CoppeliaSim funciona correctamente.
:::

---

## Reto

::: challenge
title: Explorando el Pioneer P3DX

content:

Explora detenidamente la estructura jerárquica del Pioneer P3DX.

Sin modificar ninguno de sus componentes, intenta responder a las siguientes preguntas.

- ¿Cuántas ruedas incorpora el robot?
- ¿Cuántos sensores puedes localizar?
- ¿Qué elementos parecen corresponder a scripts internos?
- ¿Qué componentes crees que utilizaremos para controlar el movimiento en los próximos capítulos?

Anota tus respuestas y compáralas posteriormente con las explicaciones que iremos desarrollando a lo largo del libro.

No es importante acertar todas las respuestas.

El objetivo consiste en comenzar a familiarizarte con la estructura interna del robot.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Presentar el Pioneer P3DX como plataforma de trabajo para el resto del libro.
- Familiarizar al alumnado con la estructura de un robot móvil.
- Verificar el correcto funcionamiento de la comunicación entre Python y CoppeliaSim.
- Realizar los primeros movimientos del robot desde programas externos.

**Material necesario**

- Ordenadores con CoppeliaSim instalado.
- Python configurado con la API remota ZeroMQ.
- Proyecto de ejemplo del capítulo.
- Proyector para realizar las demostraciones.

**Consejos metodológicos**

Dedica tiempo suficiente a que el alumnado manipule libremente el Pioneer P3DX antes de comenzar a programarlo.

Muchos errores posteriores desaparecen cuando los estudiantes comprenden cómo está organizado el robot y qué relación existe entre la escena, el árbol de objetos y el código Python.

Insiste especialmente en la diferencia entre mover un robot modificando directamente sus coordenadas y controlar realmente sus motores, ya que este concepto será fundamental en los siguientes capítulos.
:::

---

## Próximo capítulo

Ya conoces la estructura del Pioneer P3DX y eres capaz de comunicarte con él mediante Python.

Ha llegado el momento de que el robot comience a percibir el entorno.

En el siguiente capítulo aprenderás a utilizar los sensores de proximidad incorporados en el Pioneer P3DX para detectar obstáculos, medir distancias e interpretar la información del escenario.

Será el primer paso hacia el desarrollo de robots capaces de tomar decisiones de forma autónoma.