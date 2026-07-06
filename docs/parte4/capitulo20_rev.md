::: chapter-cover
number: 20
title: Manipulación de objetos con el UR3
time: 7 horas
level: ★★★★☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender el funcionamiento de una operación de **Pick & Place**.
- Preparar correctamente el UR3 para realizar tareas de manipulación.
- Instalar y ensamblar una pinza **RG2** sobre el robot.
- Comprender cómo organiza CoppeliaSim los robots y sus herramientas.
- Verificar el correcto funcionamiento de la pinza antes de programarla.
- Preparar el entorno para controlar la pinza desde Python.

:::

# Capítulo 20 · Manipulación de objetos con el UR3

## Del movimiento a la manipulación

En los capítulos anteriores hemos aprendido a controlar el robot **Universal Robots UR3** desde Python.

Primero movimos individualmente cada una de sus articulaciones y, posteriormente, utilizamos la cinemática inversa para desplazar el efector final mediante coordenadas cartesianas.

Sin embargo, un robot industrial no se instala en una fábrica únicamente para mover sus articulaciones.

Su verdadero objetivo consiste en **interactuar con objetos**.

Recoger una pieza, transportarla con precisión y depositarla en otra posición constituye una de las operaciones más habituales en cualquier proceso de automatización industrial.

Este tipo de operación recibe el nombre de **Pick & Place** y representa una de las aplicaciones más extendidas de la robótica industrial.

En este capítulo construiremos nuestra primera aplicación completa de manipulación utilizando el **UR3**, una **pinza RG2** y **Python**.

A diferencia de los capítulos anteriores, en esta ocasión prepararemos previamente el robot exactamente igual que se hace en un entorno profesional de CoppeliaSim.

::: figure
image: ../assets/cap20/fig20_1.png
caption: Operación de manipulación realizada por un robot UR3 equipado con una pinza RG2.
:::

::: teacher
content:

Antes de comenzar la práctica resulta interesante mostrar varios vídeos de aplicaciones reales de **Pick & Place** realizadas por robots colaborativos de Universal Robots.

El alumnado identificará rápidamente que la mayoría de procesos industriales consisten en repetir continuamente una misma secuencia de recogida y depósito de piezas.

:::

---

# 20.1 ¿Qué es una operación Pick & Place?

La expresión inglesa **Pick & Place** significa literalmente:

- **Pick** → recoger una pieza.
- **Place** → depositarla en otra posición.

Aunque aparentemente se trata de una tarea sencilla, una operación de manipulación requiere coordinar numerosos elementos:

- el movimiento del robot;
- la herramienta situada en el extremo del brazo;
- la trayectoria seguida durante el desplazamiento;
- la posición de la pieza;
- la seguridad frente a posibles colisiones.

En una línea de producción moderna un robot puede realizar varios miles de operaciones **Pick & Place** durante una jornada de trabajo con una precisión del orden de décimas de milímetro.

Precisamente por ello, antes de comenzar a programar conviene comprender cómo se organiza una operación completa de manipulación.

---

## Las cuatro fases de una manipulación

Prácticamente cualquier operación **Pick & Place** puede dividirse en cuatro etapas perfectamente diferenciadas.

### 1. Aproximación

El robot se desplaza hasta una posición situada sobre la pieza.

Esta posición recibe el nombre de **posición de aproximación** y permite acceder al objeto con seguridad.

### 2. Recogida

El efector final desciende verticalmente.

Cuando alcanza la altura adecuada, la pinza sujeta la pieza.

### 3. Transporte

Una vez capturada la pieza, el robot la eleva nuevamente y la desplaza hasta el punto de destino.

### 4. Depósito

El robot desciende, libera la pieza y vuelve a elevarse para abandonar la zona de trabajo sin producir colisiones.

Esta secuencia será la base de todas las aplicaciones desarrolladas durante el resto del libro.

::: figure
image: ../assets/cap20/fig20_2.png
caption: Fases principales de una operación de Pick & Place.
:::

---

## ¿Por qué siempre se aproxima desde arriba?

Uno de los errores más frecuentes cuando se comienza a programar robots consiste en mover directamente el efector final hasta la pieza siguiendo una trayectoria horizontal.

Aunque este movimiento parece más corto, presenta numerosos inconvenientes.

- Incrementa el riesgo de colisión.
- Dificulta la repetibilidad del movimiento.
- Complica el cálculo de trayectorias.
- Reduce la seguridad de la aplicación.

Por este motivo, en robótica industrial se trabaja prácticamente siempre utilizando una **posición de aproximación** situada unos centímetros por encima del objeto.

El robot desciende únicamente durante los últimos milímetros del recorrido y, una vez capturada la pieza, vuelve a elevarse antes de iniciar el desplazamiento horizontal.

Este procedimiento será una constante durante todos los capítulos dedicados a la manipulación industrial.

::: common-error
content:

Nunca programes un desplazamiento horizontal directamente hasta una pieza.

Primero aproxima el robot desde una posición elevada, desciende verticalmente y, una vez finalizada la operación, abandona la zona siguiendo el mismo recorrido.

:::

---

# 20.2 Preparación del UR3 para tareas de manipulación

Hasta ahora hemos trabajado con el modelo básico del **UR3** suministrado por CoppeliaSim.

Este modelo resulta ideal para aprender cinemática directa e inversa, pero presenta una limitación importante.

**No incorpora ninguna herramienta instalada en el extremo del robot.**

Antes de poder recoger una pieza será necesario instalar una pinza.

En este libro utilizaremos la **RG2**, una pinza paralela de dos dedos muy utilizada en aplicaciones industriales y suministrada junto con la biblioteca de modelos de CoppeliaSim.

Sin embargo, existe un detalle importante que conviene conocer.

En **CoppeliaSim Edu 4.10** la pinza **no debe conectarse arrastrándola dentro del árbol de la escena**.

Aunque visualmente pueda parecer que la herramienta queda unida al robot, el ensamblado no será correcto y la pinza aparecerá desplazada respecto al extremo del UR3.

CoppeliaSim incorpora un mecanismo específico denominado **Assembly**, diseñado precisamente para unir herramientas y robots compatibles.

Durante nuestras pruebas hemos comprobado que este es el único procedimiento que garantiza un montaje correcto de la RG2 sobre el UR3.

---

## Ensamblando correctamente la RG2

El procedimiento recomendado es el siguiente:

1. Abrir la biblioteca de modelos.
2. Acceder a:

   **Models → Components → Grippers → RG2**

3. Arrastrar la RG2 a la escena.
4. Seleccionar el modelo **RG2**.
5. Mantener pulsada la tecla **Ctrl** y seleccionar el objeto **connection** situado en el extremo del UR3.
6. Pulsar el botón **Assemble / Disassemble** de la barra de herramientas.

Tras unos instantes, CoppeliaSim colocará automáticamente la pinza en la posición y orientación correctas.

A partir de ese momento, la RG2 pasará a formar parte del robot y se moverá conjuntamente con él durante toda la simulación.

::: common-error "Muy importante"

No utilices **Set Parent** ni arrastres la pinza sobre el objeto **connection** desde el árbol de la escena.

Aunque aparentemente ambos modelos quedarán unidos, la herramienta no será ensamblada correctamente y aparecerá desplazada respecto al extremo del robot.

Utiliza siempre el botón **Assemble / Disassemble**, ya que es el procedimiento previsto por CoppeliaSim para conectar herramientas industriales.

:::

::: figure
image: ../assets/cap20/fig20_3.png
caption: Ensamblado correcto de la pinza RG2 mediante la herramienta Assemble / Disassemble.
:::

---

## Comprobando el montaje

Una vez ensamblada la pinza, el árbol de la escena mostrará la RG2 formando parte del conjunto del robot.

Aunque internamente la pinza está formada por numerosos objetos (articulaciones, sensores, scripts y puntos de unión), para el usuario funcionará como una única herramienta instalada sobre el UR3.

Antes de comenzar a programar verificaremos que el ensamblado se ha realizado correctamente y estudiaremos la estructura interna de la RG2 para comprender cómo controla CoppeliaSim su funcionamiento.

# 20.3 Conociendo la pinza RG2

Una vez ensamblada correctamente sobre el UR3, conviene dedicar unos minutos a observar cómo está construida la herramienta.

Aunque externamente la RG2 parece un único objeto, en realidad está formada por numerosos elementos que trabajan conjuntamente para simular el comportamiento de una pinza industrial real.

Comprender esta estructura facilitará enormemente la programación de aplicaciones de manipulación durante los siguientes apartados.

---

## Explorando el árbol de la escena

Si desplegamos la RG2 en el árbol jerárquico de CoppeliaSim observaremos que está formada por numerosos objetos.

Entre los más importantes destacan:

- articulaciones (*Joints*);
- sensores de fuerza (*Force Sensors*);
- sensores de proximidad;
- objetos visibles;
- un script asociado;
- puntos de unión (*attachPoint*);
- elementos auxiliares utilizados por el motor físico.

A primera vista puede parecer una estructura compleja.

Sin embargo, la mayor parte de estos objetos trabajan de forma automática y no será necesario programarlos directamente.

Nuestro objetivo consistirá únicamente en comprender qué función desempeña cada uno de ellos.

::: figure
image: ../assets/cap20/fig20_4.png
caption: Estructura interna de la pinza RG2 mostrada en el árbol de la escena.
:::

---

## El script asociado

Uno de los elementos más importantes de la RG2 es su **script asociado**.

Este script forma parte del propio modelo suministrado por CoppeliaSim y es el responsable de coordinar el funcionamiento interno de la pinza.

Gracias a este script no es necesario programar individualmente cada dedo, cada articulación o cada sensor.

Bastará con enviar una orden de apertura o cierre y el propio modelo realizará automáticamente todos los movimientos necesarios.

Esta filosofía de trabajo resulta muy habitual en CoppeliaSim.

Muchos modelos complejos incorporan scripts internos que encapsulan su funcionamiento y permiten utilizarlos como si fueran un único componente.

---

## ¿Por qué la RG2 contiene tantas articulaciones?

Si observamos detenidamente el árbol de la escena veremos que la pinza incorpora numerosas articulaciones.

Sin embargo, durante la programación no moveremos cada una de ellas de forma independiente.

La razón es sencilla.

La RG2 utiliza un mecanismo interno que sincroniza automáticamente el movimiento de ambos dedos.

Cuando uno de ellos se desplaza, el resto de articulaciones reproducen el movimiento correspondiente manteniendo el paralelismo de la pinza.

Este diseño reproduce el funcionamiento mecánico de una pinza industrial real.

::: teacher
content:

Anima al alumnado a desplegar completamente la estructura de la RG2 e identificar visualmente los diferentes tipos de objetos presentes en el modelo.

No es necesario comprender todavía el funcionamiento de cada uno de ellos.

El objetivo consiste simplemente en familiarizarse con la organización interna de los modelos complejos de CoppeliaSim.

:::

---

## Verificando el funcionamiento de la pinza

Antes de escribir nuestro primer programa en Python conviene comprobar que la pinza ha sido ensamblada correctamente.

Para ello iniciaremos la simulación mediante el botón **Play**.

Si el ensamblado se ha realizado correctamente, la RG2 permanecerá unida al extremo del UR3 durante toda la simulación.

En nuestro caso observaremos además un comportamiento interesante.

Al comenzar la simulación, la pinza ejecutará automáticamente un movimiento de cierre.

Este comportamiento confirma que el script asociado se encuentra activo y controlando correctamente la herramienta.

No es necesario intervenir manualmente.

En los siguientes apartados aprenderemos a enviar órdenes desde Python para controlar este mismo movimiento.

::: figure
image: ../assets/cap20/fig20_5.png
caption: Comprobación del funcionamiento de la RG2 tras iniciar la simulación.
:::

::: info "Observación"

Que la pinza se cierre automáticamente al iniciar la simulación es un comportamiento normal del modelo utilizado en este libro.

Este movimiento indica que el script interno de la RG2 está activo y que la herramienta ha sido ensamblada correctamente.

:::

---

# 20.4 Primer programa de control de la RG2

Una vez comprobado que la pinza funciona correctamente dentro de la simulación, ha llegado el momento de controlarla desde Python.

En los capítulos anteriores hemos aprendido a mover articulaciones individuales y a desplazar el efector final mediante cinemática inversa.

Ahora incorporaremos un nuevo elemento al sistema: la pinza.

Nuestro primer objetivo será muy sencillo.

Construiremos un programa capaz de abrir y cerrar repetidamente la RG2 para comprobar que la comunicación entre Python y CoppeliaSim funciona correctamente.

Aunque este programa todavía no manipulará ninguna pieza, servirá como base para todas las aplicaciones de **Pick & Place** desarrolladas durante el resto del capítulo.

## 20.4 Primer programa de control de la RG2

Una vez comprobado que la pinza funciona correctamente dentro de CoppeliaSim, ha llegado el momento de controlarla desde Python.

Nuestro primer objetivo será muy sencillo.

No moveremos todavía el robot.

Simplemente construiremos un programa capaz de abrir y cerrar la RG2 de forma repetitiva para verificar que la comunicación entre Python y la simulación funciona correctamente.

Este pequeño programa será la base sobre la que construiremos posteriormente toda la aplicación de **Pick & Place**.

---

## Conectando con CoppeliaSim

Como en los capítulos anteriores, el primer paso consiste en establecer la conexión con CoppeliaSim mediante la **ZeroMQ Remote API**.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")
```

Una vez ejecutadas estas instrucciones, el programa ya puede acceder a todos los objetos de la escena y controlar la simulación desde Python.

---

## Comprobando el estado de la simulación

Antes de enviar órdenes a la pinza resulta conveniente comprobar si la simulación se encuentra en funcionamiento.

Si estuviera detenida, nuestro programa la iniciará automáticamente.

```python
estado = sim.getSimulationState()

if estado == sim.simulation_stopped:
    sim.startSimulation()
    time.sleep(1)
```

Este procedimiento evita que el usuario tenga que iniciar manualmente la simulación cada vez que ejecuta el programa.

Además, garantiza que la pinza y el resto de componentes estén preparados para recibir órdenes.

::: figure
image: ../assets/cap20/fig20_6.png
caption: Inicio automático de la simulación antes de controlar la pinza.
:::

---

## Localizando la RG2

El siguiente paso consiste en comprobar que la pinza se encuentra correctamente instalada en la escena.

Dependiendo de la versión de CoppeliaSim o de la estructura del árbol, la RG2 puede aparecer en distintas posiciones.

Por este motivo, nuestro programa comprobará automáticamente varias rutas posibles hasta localizarla.

Esta estrategia hace que el código sea mucho más robusto y facilita su reutilización en diferentes escenas.

```python
RUTAS_RG2 = [
    "/RG2",
    "/UR3/connection/RG2",
    "/UR3/RG2",
]
```

Posteriormente se recorrerán todas estas rutas hasta encontrar el modelo instalado.

Si alguna de ellas existe, el programa continuará automáticamente.

En caso contrario mostrará un mensaje informando de que la pinza no ha podido localizarse.

Esta forma de trabajar resulta muy recomendable cuando se desarrollan aplicaciones reutilizables.

::: info "Buena práctica"

Siempre que sea posible evita asumir que un objeto se encuentra en una única posición del árbol.

Comprobar varias rutas posibles hace que el programa sea mucho más flexible y reutilizable.

:::

---

## Localizando las articulaciones de la pinza

Aunque la RG2 funciona como una única herramienta, internamente está formada por varias articulaciones.

Nuestro programa localizará automáticamente aquellas que intervienen en el movimiento de apertura y cierre.

Una vez obtenidos sus identificadores, podrá enviarles órdenes de velocidad y fuerza sin necesidad de conocer previamente la estructura exacta del modelo.

Este procedimiento hace que el mismo programa pueda utilizarse con pequeñas variaciones del modelo RG2 sin necesidad de modificar el código.

::: figure
image: ../assets/cap20/fig20_7.png
caption: Localización automática de las articulaciones internas de la RG2.
:::

---

## Controlando el movimiento de la pinza

Una vez localizadas las articulaciones, podremos controlar su movimiento.

Para ello definiremos tres parámetros fundamentales.

```python
VELOCIDAD_APERTURA = 0.04
VELOCIDAD_CIERRE = -0.04
FUERZA_PINZA = 20
```

Estos valores determinan:

- la velocidad con la que se abrirá la pinza;
- la velocidad con la que se cerrará;
- la fuerza máxima aplicada por el mecanismo.

Modificando estos parámetros podremos adaptar fácilmente el comportamiento de la herramienta a diferentes aplicaciones.

---

## Las funciones abrir_pinza() y cerrar_pinza()

Para simplificar la lectura del programa agruparemos todas las operaciones de apertura y cierre dentro de dos funciones.

De este modo el resto del código será mucho más claro.

Conceptualmente, su funcionamiento puede resumirse de la siguiente forma.

```text
abrir_pinza()

↓

activar apertura

↓

mover articulaciones

↓

pinza abierta
```

y

```text
cerrar_pinza()

↓

activar cierre

↓

mover articulaciones

↓

pinza cerrada
```

Más adelante reutilizaremos estas mismas funciones durante todas las operaciones de **Pick & Place**, evitando repetir continuamente las mismas instrucciones.

---

## Primer ciclo de prueba

Una vez construidas ambas funciones, comprobar el funcionamiento de la pinza resulta muy sencillo.

Basta con ejecutarlas alternativamente dejando una pequeña pausa entre ambas.

```python
while True:

    abrir_pinza()
    time.sleep(2)

    cerrar_pinza()
    time.sleep(2)
```

Al ejecutar este programa observaremos cómo la RG2 abre y cierra sus dedos continuamente.

Aunque todavía no estamos manipulando ninguna pieza, esta prueba confirma que:

- la comunicación con CoppeliaSim funciona correctamente;
- la RG2 ha sido ensamblada correctamente;
- Python puede controlar la herramienta.

Hemos completado así el primer paso para desarrollar una aplicación completa de manipulación industrial.

::: figure
image: ../assets/cap20/fig20_8.png
caption: Programa de prueba realizando ciclos continuos de apertura y cierre de la RG2.
:::

::: teacher
content:

Antes de continuar con el movimiento del robot, pide al alumnado que experimente modificando los valores de velocidad y fuerza de la pinza.

Este sencillo ejercicio permite comprender la influencia que tienen estos parámetros sobre el comportamiento de la herramienta y prepara el terreno para las aplicaciones de manipulación que desarrollaremos en los siguientes apartados.

:::

# 20.5 Integrando el movimiento del UR3 y la RG2

Hasta este momento hemos trabajado por separado con los dos elementos principales de nuestra aplicación.

Por una parte, el **UR3**, cuyo efector final puede desplazarse mediante cinemática inversa modificando la posición del objeto `UR3_target`.

Por otra, la **pinza RG2**, que ya somos capaces de abrir y cerrar desde Python.

Ha llegado el momento de combinar ambos sistemas para construir una verdadera aplicación de manipulación.

---

## Dos sistemas que trabajan conjuntamente

Aunque durante la simulación parece que el robot constituye un único mecanismo, realmente intervienen dos sistemas independientes.

El primero es el encargado de mover el brazo mediante cinemática inversa.

El segundo controla la apertura y el cierre de la pinza.

Nuestro programa será el encargado de coordinar ambos.

Podemos representar esta relación mediante el siguiente esquema.

```text
Python
   │
   ├──────────────► UR3_target
   │                     │
   │                     ▼
   │             Cinemática inversa
   │                     │
   │                     ▼
   │                  Robot UR3
   │
   └──────────────► RG2
                         │
                         ▼
                Apertura / cierre
```

A partir de este momento el robot dejará de realizar simples movimientos para comenzar a interactuar con los objetos presentes en la escena.

::: figure
image: ../assets/cap20/fig20_9.png
caption: Coordinación entre el movimiento del UR3 y el accionamiento de la pinza RG2.
:::

---

## Definiendo las posiciones de trabajo

Como vimos en el capítulo anterior, el movimiento cartesiano del UR3 se realiza modificando la posición del objeto **UR3_target**.

Para construir una operación de **Pick & Place** definiremos cuatro posiciones fundamentales.

```python
APROX_ORIGEN = [0.35, -0.15, 0.30]
RECOGIDA     = [0.35, -0.15, 0.20]

APROX_DESTINO = [0.10, 0.20, 0.30]
DEPOSITO      = [0.10, 0.20, 0.20]
```

Las posiciones de aproximación se encuentran unos centímetros por encima de la pieza.

Las posiciones de recogida y depósito corresponden al punto exacto donde la pinza debe sujetar o liberar el objeto.

Esta organización facilita enormemente la programación y reduce el riesgo de colisiones.

---

## ¿Por qué utilizamos cuatro posiciones?

Podría parecer suficiente definir únicamente el punto de recogida y el punto de depósito.

Sin embargo, hacerlo así obligaría al robot a desplazarse horizontalmente muy cerca de la mesa de trabajo.

Esta situación incrementaría notablemente el riesgo de colisión.

Utilizando posiciones de aproximación conseguimos que todos los desplazamientos horizontales se realicen a una altura segura.

Únicamente durante los últimos centímetros el robot desciende verticalmente para manipular la pieza.

Este procedimiento reproduce la forma de trabajar utilizada en la mayoría de robots industriales.

::: figure
image: ../assets/cap20/fig20_10.png
caption: Utilización de posiciones de aproximación para evitar colisiones durante la manipulación.
:::

---

## La secuencia completa de una manipulación

Una vez definidas las posiciones de trabajo y controlada la pinza, la operación completa puede resumirse mediante la siguiente secuencia.

```text
1. Abrir la RG2

2. Ir a la posición de aproximación

3. Descender hasta la pieza

4. Cerrar la RG2

5. Elevar la pieza

6. Desplazarse al destino

7. Descender

8. Abrir la RG2

9. Elevar el robot
```

Observa que todas las operaciones siguen exactamente el mismo patrón.

Este hecho permitirá reutilizar posteriormente el mismo algoritmo para manipular cualquier número de piezas.

---

## Programando mediante funciones

En lugar de escribir una larga lista de instrucciones, resulta mucho más conveniente dividir el programa en pequeñas funciones.

Por ejemplo:

- `mover_target()`
- `abrir_pinza()`
- `cerrar_pinza()`
- `esperar_robot()`

Cada una de ellas realizará una única tarea perfectamente definida.

Posteriormente podremos combinarlas para construir aplicaciones cada vez más complejas.

Esta forma de trabajar mejora considerablemente la legibilidad del código y facilita su mantenimiento.

::: info "Programación modular"

La programación modular constituye una de las técnicas más utilizadas en robótica industrial.

Dividir una aplicación en pequeñas funciones reutilizables permite construir programas complejos de forma mucho más sencilla y facilita enormemente la localización de errores.

:::

---

## Preparando nuestro primer Pick & Place

Ya disponemos de todos los elementos necesarios.

Sabemos:

- mover el UR3 mediante cinemática inversa;
- abrir y cerrar la RG2;
- definir posiciones de aproximación;
- organizar el programa mediante funciones.

En el siguiente apartado construiremos nuestro primer ciclo completo de manipulación.

Por primera vez el UR3 será capaz de recoger una pieza, transportarla y depositarla automáticamente en otra posición.

::: teacher
content:

Antes de comenzar la programación del ciclo completo, resulta recomendable ejecutar varias veces únicamente los movimientos del robot entre las posiciones de aproximación y recogida.

De este modo el alumnado comprobará que todas las trayectorias son correctas antes de incorporar el accionamiento de la pinza.

Este procedimiento reduce considerablemente los errores de programación y reproduce la metodología utilizada durante la puesta en marcha de una célula robotizada real.

:::

# 20.6 Construyendo nuestro primer ciclo de Pick & Place

Después de preparar el UR3, ensamblar correctamente la pinza RG2 y comprobar que somos capaces de controlarla desde Python, ha llegado el momento de construir una aplicación completa de manipulación.

Nuestro objetivo será desarrollar un programa capaz de realizar automáticamente la siguiente secuencia:

1. Aproximarse a la pieza.
2. Descender hasta la posición de recogida.
3. Sujetar la pieza con la RG2.
4. Elevar la pieza.
5. Transportarla hasta el destino.
6. Depositarla.
7. Regresar a una posición segura.

Aunque la secuencia parece sencilla, integra todos los conocimientos adquiridos durante los capítulos anteriores.

---

## El algoritmo de trabajo

Antes de escribir una sola línea de código conviene definir claramente el algoritmo que seguirá el robot.

```text
Abrir RG2

↓

Ir a la aproximación del origen

↓

Descender hasta la pieza

↓

Cerrar RG2

↓

Esperar

↓

Elevar la pieza

↓

Ir a la aproximación del destino

↓

Descender

↓

Abrir RG2

↓

Esperar

↓

Elevar el robot
```

Una vez comprendida esta secuencia, traducirla a Python resulta mucho más sencillo.

::: figure
image: ../assets/cap20/fig20_11.png
caption: Algoritmo completo de una operación de Pick & Place.
:::

---

## Construyendo la secuencia paso a paso

La primera versión del programa seguirá exactamente el orden definido anteriormente.

```python
abrir_pinza()

mover_target(APROX_ORIGEN)

mover_target(RECOGIDA)

cerrar_pinza()

time.sleep(1)

mover_target(APROX_ORIGEN)

mover_target(APROX_DESTINO)

mover_target(DEPOSITO)

abrir_pinza()

time.sleep(1)

mover_target(APROX_DESTINO)
```

Aunque el programa es muy corto, el UR3 ejecutará una operación completa de manipulación.

Cada instrucción corresponde exactamente a una de las etapas estudiadas anteriormente.

---

## Analizando el programa

Observemos con detenimiento qué ocurre durante la ejecución.

### Abrir la pinza

La primera instrucción garantiza que la RG2 se encuentra preparada para recoger la pieza.

```python
abrir_pinza()
```

Este paso resulta imprescindible.

Si la pinza permaneciera cerrada, el robot no podría capturar correctamente el objeto.

---

### Aproximación

A continuación el UR3 se desplaza hasta una posición situada sobre la pieza.

```python
mover_target(APROX_ORIGEN)
```

Todavía no existe contacto con el objeto.

Únicamente estamos preparando el descenso.

---

### Descenso

El siguiente movimiento sitúa la pinza exactamente sobre la pieza.

```python
mover_target(RECOGIDA)
```

Ahora sí se alcanza la posición donde debe producirse la manipulación.

---

### Captura de la pieza

Una vez detenido el robot, la RG2 cierra sus dedos.

```python
cerrar_pinza()
```

Añadimos además una pequeña pausa.

```python
time.sleep(1)
```

Aunque en una simulación el movimiento es muy rápido, esta espera mejora la estabilidad del proceso y reproduce el comportamiento habitual de una instalación industrial.

---

### Transporte

Una vez capturada la pieza, el robot vuelve a elevarse.

```python
mover_target(APROX_ORIGEN)
```

A continuación se desplaza hasta el destino.

```python
mover_target(APROX_DESTINO)
```

Observa que todo el desplazamiento horizontal se realiza a una altura segura.

---

### Depósito

El robot desciende.

```python
mover_target(DEPOSITO)
```

Abre la pinza.

```python
abrir_pinza()
```

Espera brevemente.

```python
time.sleep(1)
```

Y finalmente vuelve a elevarse.

```python
mover_target(APROX_DESTINO)
```

La operación de **Pick & Place** ha concluido correctamente.

::: figure
image: ../assets/cap20/fig20_12.png
caption: Ejecución completa de una operación de Pick & Place utilizando el UR3 y la RG2.
:::

---

## Comprobando el resultado

Si todo ha funcionado correctamente podremos observar que:

- la RG2 permanece abierta al finalizar la operación;
- el UR3 regresa a una posición segura;
- la pieza queda situada en el punto de destino;
- durante toda la trayectoria el robot evita desplazamientos horizontales próximos a la mesa.

Si alguno de estos puntos no se cumple, conviene revisar las coordenadas de trabajo antes de continuar.

::: common-error
content:

Uno de los errores más frecuentes consiste en definir una posición de aproximación demasiado baja.

Como consecuencia, el robot puede golpear la pieza durante el desplazamiento horizontal.

Siempre que sea posible utiliza una altura suficiente para evitar cualquier riesgo de colisión.

:::

---

## ¿Podemos reutilizar este programa?

La respuesta es sí.

De hecho, éste es precisamente uno de los principios fundamentales de la programación industrial.

Si observamos el programa veremos que toda la operación constituye una única tarea perfectamente definida.

Por tanto, en lugar de copiar continuamente estas instrucciones, resulta mucho más conveniente agruparlas dentro de una función reutilizable.

Éste será precisamente el siguiente paso.

# 20.7 Automatizando la operación de Pick & Place

Hasta ahora nuestro programa realiza una única operación de manipulación.

Una vez finalizada la secuencia, el robot permanece detenido esperando una nueva orden.

Sin embargo, en una instalación industrial real esto rara vez ocurre.

Los robots industriales suelen repetir continuamente la misma operación mientras existan piezas que manipular.

Nuestro siguiente objetivo consistirá en convertir la secuencia desarrollada anteriormente en un ciclo completamente automático.

---

## Reutilizando el código

Si observamos el programa desarrollado en el apartado anterior comprobaremos que todas las instrucciones pertenecen a una única tarea.

Recoger una pieza y depositarla en otra posición.

En programación resulta poco recomendable copiar continuamente el mismo bloque de instrucciones.

La solución consiste en agrupar toda la secuencia dentro de una función.

```python
def pick_and_place():

    abrir_pinza()

    mover_target(APROX_ORIGEN)

    mover_target(RECOGIDA)

    cerrar_pinza()

    time.sleep(1)

    mover_target(APROX_ORIGEN)

    mover_target(APROX_DESTINO)

    mover_target(DEPOSITO)

    abrir_pinza()

    time.sleep(1)

    mover_target(APROX_DESTINO)
```

A partir de este momento, ejecutar una operación completa de manipulación será tan sencillo como llamar a esta función.

```python
pick_and_place()
```

La ventaja de este planteamiento es evidente.

Si en el futuro deseamos modificar la forma en que el robot manipula una pieza únicamente tendremos que cambiar el contenido de esta función.

El resto del programa permanecerá exactamente igual.

::: figure
image: ../assets/cap20/fig20_13.png
caption: Organización de toda la secuencia de manipulación dentro de una función reutilizable.
:::

---

## Ejecutando varias operaciones consecutivas

Una vez creada la función, automatizar el trabajo del robot resulta muy sencillo.

Basta con ejecutarla repetidamente.

```python
while True:

    pick_and_place()
```

Con estas dos líneas el UR3 repetirá continuamente la misma operación mientras la simulación permanezca activa.

Este tipo de estructura constituye uno de los patrones de programación más habituales en robótica industrial.

---

## ¿Cómo finaliza el ciclo?

En nuestro ejemplo el bucle se ejecuta indefinidamente.

Sin embargo, en una aplicación industrial real el robot dejará de trabajar cuando se produzca alguna de las siguientes situaciones:

- no existan más piezas para manipular;
- un sensor detecte una incidencia;
- el operario pulse el botón de parada;
- aparezca una condición de emergencia;
- finalice la orden de fabricación.

Durante este capítulo utilizaremos un ciclo continuo para simplificar el aprendizaje.

En los próximos capítulos incorporaremos sensores que decidirán automáticamente cuándo debe comenzar o detenerse una operación de manipulación.

::: figure
image: ../assets/cap20/fig20_14.png
caption: Ejecución continua de la función `pick_and_place()` mediante un bucle infinito.
:::

---

## Ventajas de la programación modular

Dividir el programa en pequeñas funciones independientes aporta numerosas ventajas.

- El código resulta más sencillo de leer.
- Facilita la localización de errores.
- Permite reutilizar funciones en diferentes proyectos.
- Reduce la duplicación de código.
- Simplifica el mantenimiento de la aplicación.

Esta forma de trabajar será la utilizada durante el resto del libro.

De hecho, en los siguientes capítulos continuaremos ampliando la aplicación incorporando sensores, cintas transportadoras y nuevas operaciones sin necesidad de modificar la estructura básica del programa.

::: teacher
content:

Antes de continuar, pide al alumnado que modifique únicamente las coordenadas de recogida y depósito.

Comprobarán que la función `pick_and_place()` continúa funcionando correctamente sin necesidad de modificar ninguna otra parte del programa.

Este ejercicio permite comprender una de las principales ventajas de la programación modular.

:::

---

## Hacia una célula robotizada

Hasta este momento el UR3 ha trabajado con una única pieza situada en una posición fija.

Aunque este tipo de ejercicios resulta ideal para comprender la lógica de una operación de manipulación, no representa todavía una instalación industrial completa.

En una célula robotizada real las piezas llegan continuamente mediante una cinta transportadora.

Diversos sensores detectan su presencia y el robot únicamente inicia el movimiento cuando las condiciones de trabajo son correctas.

Además, pueden intervenir cámaras de visión artificial, lectores de códigos, sistemas de clasificación o incluso otros robots colaborando simultáneamente.

Todos estos elementos serán incorporados progresivamente durante los siguientes capítulos.

La aplicación desarrollada en este capítulo constituirá el núcleo sobre el que construiremos una célula robotizada completa.

::: info "Lo que hemos conseguido"

A partir de este momento ya disponemos de todos los elementos necesarios para desarrollar aplicaciones reales de manipulación:

- controlar el movimiento cartesiano del UR3;
- abrir y cerrar la pinza RG2;
- definir posiciones de aproximación;
- organizar el código mediante funciones;
- automatizar un ciclo completo de Pick & Place.

En los próximos capítulos ampliaremos este sistema incorporando nuevos elementos de automatización industrial.

:::

# 20.8 Buenas prácticas y resolución de problemas

Después de completar nuestro primer programa de **Pick & Place**, conviene detenerse unos minutos para revisar una serie de recomendaciones que facilitarán el desarrollo de aplicaciones de manipulación más complejas.

La mayoría de errores que aparecen durante las primeras prácticas no están relacionados con la programación, sino con una preparación incorrecta de la escena o con una planificación inadecuada de las trayectorias.

Conocer estos problemas desde el principio permitirá ahorrar mucho tiempo durante el desarrollo de futuros proyectos.

---

## Buenas prácticas

A lo largo de este capítulo hemos seguido una metodología que conviene mantener en todas las aplicaciones de manipulación.

### Ensambla siempre correctamente la herramienta

Antes de escribir una sola línea de código verifica que la pinza ha sido instalada utilizando el procedimiento **Assemble / Disassemble**.

No utilices el comando **Set Parent** para unir la RG2 al robot.

Aunque ambos modelos parezcan conectados, el ensamblado no será correcto.

---

### Comprueba el funcionamiento de la pinza antes de mover el robot

Una práctica muy recomendable consiste en desarrollar primero un pequeño programa que únicamente abra y cierre la RG2.

Si la herramienta responde correctamente, será mucho más sencillo localizar posibles errores cuando posteriormente se incorpore el movimiento del UR3.

---

### Verifica siempre las posiciones de aproximación

Antes de ejecutar un ciclo completo comprueba que las posiciones de aproximación se encuentran suficientemente elevadas.

De este modo evitarás que el robot golpee accidentalmente la pieza o la superficie de trabajo durante los desplazamientos horizontales.

---

### Trabaja mediante funciones

Agrupar las distintas operaciones dentro de funciones independientes simplifica enormemente el programa.

En este capítulo hemos utilizado funciones como:

- `abrir_pinza()`
- `cerrar_pinza()`
- `mover_target()`
- `pick_and_place()`

Esta organización facilita el mantenimiento del código y permitirá ampliar la aplicación en los siguientes capítulos.

::: figure
image: ../assets/cap20/fig20_15.png
caption: Organización modular del programa de manipulación.
:::

---

# Problemas frecuentes

Durante el desarrollo de este capítulo pueden aparecer algunas incidencias habituales.

Las siguientes recomendaciones recogen los problemas más comunes detectados durante las pruebas realizadas con **CoppeliaSim Edu 4.10**.

---

## La pinza aparece desplazada respecto al extremo del robot

**Causa**

La RG2 se ha unido al UR3 mediante **Set Parent** o arrastrándola directamente sobre el objeto `connection`.

**Solución**

Eliminar la pinza de la escena y volver a ensamblarla utilizando el botón **Assemble / Disassemble**.

---

## La RG2 no responde desde Python

**Causa**

La simulación no está iniciada o el programa no consigue localizar correctamente la pinza.

**Solución**

- comprobar que la simulación está en ejecución;
- verificar que la RG2 aparece correctamente ensamblada;
- revisar las rutas utilizadas para localizar el modelo.

---

## El robot golpea la pieza durante el desplazamiento

**Causa**

Las posiciones de aproximación se encuentran demasiado próximas a la superficie de trabajo.

**Solución**

Incrementar la coordenada **Z** de las posiciones de aproximación hasta garantizar un desplazamiento seguro.

---

## La pieza no queda correctamente depositada

**Causa**

La pinza se abre antes de alcanzar la posición de depósito.

**Solución**

Comprobar que el robot ha finalizado completamente el descenso antes de ejecutar `abrir_pinza()`.

---

## El movimiento resulta poco natural

**Causa**

Las velocidades de apertura de la RG2 o las pausas entre movimientos son demasiado pequeñas.

**Solución**

Modificar los parámetros de velocidad y los tiempos de espera hasta obtener un comportamiento más suave.

::: teacher
content:

Anima al alumnado a provocar deliberadamente alguno de estos errores y posteriormente corregirlo.

Aprender a diagnosticar incidencias constituye una parte fundamental de la programación de robots industriales.

:::

---

---

# 20.9 Práctica guiada · Primer sistema de manipulación con el UR3 y la RG2

::: practice
title: Construcción de un sistema básico de Pick & Place

difficulty: Media

time: 90 minutos

content:

En esta práctica integrarás todos los conocimientos adquiridos a lo largo del capítulo para construir una aplicación básica de manipulación utilizando el robot **UR3**, una **pinza RG2** y **Python**.

### Objetivos

Al finalizar la práctica serás capaz de:

- ensamblar correctamente una RG2 sobre el UR3;
- comprobar el funcionamiento de la pinza;
- controlar su apertura y cierre desde Python;
- desplazar el efector final mediante cinemática inversa;
- desarrollar una operación completa de **Pick & Place**.

### Actividades

1. Abre la escena del UR3 utilizada durante este capítulo.
2. Inserta una **RG2** desde la biblioteca de modelos.
3. Ensámblala correctamente utilizando **Assemble / Disassemble**.
4. Comprueba que la pinza permanece unida al robot durante la simulación.
5. Ejecuta el programa de apertura y cierre de la RG2.
6. Define las posiciones de aproximación, recogida y depósito.
7. Programa una operación completa de **Pick & Place**.
8. Repite la operación modificando únicamente las coordenadas de destino.
9. Ajusta las velocidades del robot y de la pinza para obtener un movimiento más suave.
10. Comprueba que todas las trayectorias se realizan sin colisiones.

### Resultado esperado

El UR3 deberá recoger automáticamente una pieza, transportarla hasta otra posición y depositarla utilizando la pinza RG2, manteniendo en todo momento trayectorias seguras.

:::

---

# Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.

content:

| Concepto | Descripción |
|-----------|-------------|
| Pick & Place | Operación de recoger una pieza y depositarla en otra posición. |
| RG2 | Pinza paralela utilizada como efector final del UR3. |
| Assemble / Disassemble | Herramienta de CoppeliaSim para ensamblar correctamente modelos compatibles. |
| Position de aproximación | Punto situado por encima de la pieza para evitar colisiones. |
| Efector final | Herramienta instalada en el extremo del robot. |
| Trayectoria cartesiana | Movimiento del efector final en coordenadas XYZ. |
| Programación modular | Organización del código mediante funciones reutilizables. |
| Pick & Place automático | Secuencia repetitiva de manipulación ejecutada por el robot. |

:::

---

# En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender las fases de una operación de **Pick & Place**.
- ✅ Preparar correctamente un UR3 para realizar tareas de manipulación.
- ✅ Ensamblar una pinza **RG2** utilizando **Assemble / Disassemble**.
- ✅ Comprender la estructura interna de la RG2.
- ✅ Verificar el funcionamiento de la pinza antes de programarla.
- ✅ Controlar la RG2 desde Python.
- ✅ Coordinar el movimiento cartesiano del UR3 con la apertura y el cierre de la pinza.
- ✅ Construir un ciclo completo de manipulación.
- ✅ Organizar la aplicación mediante funciones reutilizables.

---

# Autoevaluación

Responde a las siguientes preguntas sin consultar el contenido del capítulo.

1. ¿Qué diferencia existe entre el movimiento del UR3 y la manipulación de una pieza?
2. ¿Qué significa la expresión **Pick & Place**?
3. ¿Por qué es recomendable utilizar posiciones de aproximación?
4. ¿Qué procedimiento debe utilizarse para montar correctamente una RG2 sobre el UR3?
5. ¿Por qué no debe utilizarse **Set Parent** para unir la pinza al robot?
6. ¿Qué función desempeña el script interno de la RG2?
7. ¿Qué ventajas ofrece dividir el programa en funciones reutilizables?
8. ¿Qué ocurriría si el robot realizara el desplazamiento horizontal demasiado cerca de la mesa?
9. ¿Qué ventajas aporta automatizar el ciclo de manipulación?
10. ¿Qué modificarías para reutilizar el mismo programa con otra posición de recogida?

---

# Reto

::: challenge
title: Clasificación automática de piezas

content:

Amplía la aplicación desarrollada durante este capítulo para que el UR3 manipule varias piezas situadas en posiciones diferentes.

Como ampliación:

- utiliza varias posiciones de recogida;
- crea varias posiciones de depósito;
- reutiliza la misma función `pick_and_place()`;
- añade una pausa configurable entre ciclos;
- intenta organizar todas las posiciones mediante listas o diccionarios para evitar duplicar código.

:::

---

# Para el profesor

::: teacher
title: Orientaciones didácticas

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Consolidar la cinemática inversa del UR3.
- Comprender el montaje correcto de herramientas en CoppeliaSim.
- Introducir el control coordinado entre robot y pinza.
- Familiarizar al alumnado con la programación modular.

**Aspectos que conviene reforzar**

- Ensamblar siempre la RG2 mediante **Assemble / Disassemble**.
- Verificar el funcionamiento de la pinza antes de comenzar a programar.
- Utilizar posiciones de aproximación para evitar colisiones.
- Analizar la secuencia completa antes de escribir el código.

**Errores frecuentes**

- Intentar unir la pinza mediante **Set Parent**.
- Desplazar el robot horizontalmente demasiado cerca de la pieza.
- No esperar a que la pinza termine de cerrar antes de elevar el robot.
- No comprobar que la simulación está iniciada antes de ejecutar el programa.

:::

---

# Próximo capítulo

En este capítulo hemos aprendido a controlar un robot industrial y una pinza como un único sistema de manipulación.

En el siguiente capítulo incorporaremos nuevos elementos de automatización para construir aplicaciones todavía más realistas, integrando el UR3 con otros componentes de una célula robotizada y ampliando las capacidades del sistema de manipulación desarrollado hasta ahora.