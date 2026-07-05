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

- Comprender las fases de una operación de manipulación industrial.
- Controlar el UR3 para recoger y depositar objetos.
- Planificar trayectorias seguras de aproximación y retirada.
- Coordinar el movimiento del robot con una pinza.
- Programar secuencias completas de **pick & place** desde Python.
- Desarrollar aplicaciones básicas de automatización industrial en CoppeliaSim.

:::

# Capítulo 20 · Manipulación de objetos con el UR3

## Del movimiento a la manipulación

Durante los dos capítulos anteriores hemos aprendido a controlar el **Universal Robots UR3**.

Primero movimos individualmente sus articulaciones y, posteriormente, utilizamos la cinemática inversa para desplazar el efector final mediante coordenadas cartesianas.

Sin embargo, mover un robot no constituye un objetivo por sí mismo.

En la industria, los robots existen para realizar tareas útiles.

Una de las más habituales consiste en **manipular objetos**.

Recoger una pieza, trasladarla hasta otro punto y depositarla con precisión son operaciones presentes en prácticamente cualquier proceso automatizado.

En este capítulo aprenderemos a desarrollar este tipo de aplicaciones utilizando CoppeliaSim y Python.

::: figure
image: ../assets/cap20/fig20_1.png
caption: Operación de manipulación realizada por el UR3 desplazando una pieza entre dos posiciones.
:::

::: teacher
content:

Antes de comenzar la programación, muestra al alumnado varios vídeos cortos de aplicaciones reales del UR3 en tareas de montaje, clasificación o empaquetado.

Esto ayudará a relacionar inmediatamente los ejercicios del capítulo con situaciones industriales reales.

:::

---

## 20.1 ¿Qué es una operación *pick & place*?

La operación **pick & place** constituye una de las aplicaciones más comunes de la robótica industrial.

Su nombre proviene del inglés y significa literalmente:

- **Pick** → recoger una pieza.
- **Place** → depositarla en otro lugar.

Aunque aparentemente se trata de una tarea sencilla, implica coordinar numerosos elementos:

- el movimiento del robot;
- la apertura y cierre de la pinza;
- la trayectoria seguida por el efector final;
- la posición exacta de la pieza;
- la seguridad durante todo el recorrido.

En una fábrica moderna, miles de operaciones de este tipo pueden realizarse cada hora con una precisión de décimas o incluso centésimas de milímetro.

---

### Las cuatro fases de una manipulación

Toda operación de **pick & place** puede dividirse en cuatro etapas principales.

1. **Aproximación**

   El robot se desplaza hasta una posición situada justo encima de la pieza.

2. **Recogida**

   El efector final desciende, la pinza sujeta el objeto y confirma que la pieza ha sido capturada.

3. **Transporte**

   El UR3 eleva nuevamente la pieza y la desplaza hasta el punto de destino.

4. **Depósito**

   El robot desciende, libera la pieza y regresa a una posición segura para comenzar un nuevo ciclo.

Esta secuencia será la base de prácticamente todas las aplicaciones que desarrollaremos durante este capítulo.

::: figure
image: ../assets/cap20/fig20_2.png
caption: Fases principales de una operación de **pick & place** con el UR3.
:::

---

### ¿Por qué no se mueve directamente hasta la pieza?

Puede parecer más rápido desplazar el robot directamente hasta el objeto.

Sin embargo, esta estrategia resulta poco recomendable.

En la práctica industrial siempre se utiliza una **posición de aproximación** situada por encima de la pieza.

Este procedimiento ofrece numerosas ventajas.

- Reduce el riesgo de colisión.
- Facilita la repetibilidad del movimiento.
- Permite aproximarse verticalmente al objeto.
- Simplifica la programación de trayectorias.
- Hace que el proceso sea más seguro y predecible.

Por este motivo, durante todo el libro trabajaremos siempre utilizando posiciones de aproximación antes de recoger o depositar una pieza.

::: common-error
content:

Uno de los errores más habituales consiste en desplazar el efector final directamente hasta la pieza siguiendo una trayectoria horizontal.

Este tipo de movimientos aumenta considerablemente el riesgo de colisiones con otros objetos de la escena.

Siempre que sea posible, aproxima el robot desde arriba y retíralo siguiendo el mismo recorrido.

:::

---

### Lo que construiremos en este capítulo

A lo largo de este capítulo desarrollaremos progresivamente una aplicación completa de manipulación.

Comenzaremos moviendo el UR3 hasta una pieza.

Posteriormente aprenderemos a controlar la pinza, sincronizar su apertura y cierre con el movimiento del robot y, finalmente, construiremos una secuencia automática capaz de recoger y depositar objetos de forma repetitiva.

Al finalizar el capítulo habrás desarrollado tu primera aplicación de manipulación industrial utilizando CoppeliaSim y Python, empleando una metodología muy similar a la utilizada en instalaciones industriales reales.

---

## 20.2 El efector final: la pinza del UR3

Hasta ahora hemos considerado que el extremo del robot era simplemente un punto que podía desplazarse por el espacio.

Sin embargo, un robot industrial necesita una herramienta que le permita interactuar con su entorno.

Esta herramienta recibe el nombre de **efector final** (*End Effector*).

Dependiendo de la aplicación, el efector final puede adoptar formas muy diferentes.

En nuestro caso utilizaremos una **pinza paralela de dos dedos**, ideal para sujetar pequeñas piezas prismáticas y cilíndricas.

::: figure
image: ../assets/cap20/fig20_3.png
caption: Pinza paralela montada en el efector final del UR3.
:::

---

### ¿Qué funciones realiza una pinza?

Aunque su funcionamiento parece sencillo, la pinza desempeña un papel fundamental durante toda la operación de manipulación.

Sus principales funciones son:

- sujetar la pieza con seguridad;
- mantenerla estable durante el transporte;
- liberarla en la posición deseada;
- evitar que la pieza se desplace o caiga.

La calidad de una operación de **pick & place** depende tanto del movimiento del robot como del correcto funcionamiento de la pinza.

---

## Apertura y cierre

Durante una operación de manipulación la pinza únicamente realiza dos acciones básicas:

- **Abrirse** para permitir la entrada o salida de la pieza.
- **Cerrarse** para sujetarla con firmeza.

Aunque en una instalación industrial existen sensores que verifican si la pieza ha sido capturada correctamente, en nuestras primeras prácticas utilizaremos un funcionamiento simplificado.

El objetivo será comprender la coordinación entre el movimiento del robot y la apertura o cierre de la pinza.

::: figure
image: ../assets/cap20/fig20_4.png
caption: Estados principales de una pinza paralela: abierta y cerrada.
:::

---

### Coordinación entre robot y pinza

Mover correctamente el robot no es suficiente.

La apertura y el cierre de la pinza deben producirse en el momento adecuado.

Una secuencia típica es la siguiente:

1. El UR3 se aproxima a la pieza.
2. La pinza permanece abierta.
3. El robot desciende lentamente.
4. La pinza se cierra sujetando la pieza.
5. El robot eleva nuevamente la carga.

Esta coordinación evita esfuerzos innecesarios y reduce el riesgo de perder la pieza durante el transporte.

---

### Una secuencia sincronizada

Podemos representar una operación completa mediante la siguiente secuencia temporal:

```text
Aproximación
      │
      ▼
Pinza abierta
      │
      ▼
Descenso
      │
      ▼
Cierre de la pinza
      │
      ▼
Elevación
      │
      ▼
Transporte
```

Observa que la pinza **no se cierra inmediatamente al llegar sobre la pieza**.

Primero el robot debe descender hasta la altura correcta y solo entonces sujetar el objeto.

Este detalle resulta esencial para conseguir movimientos fiables y repetibles.

::: teacher
content:

Pide al alumnado que ejecute lentamente la secuencia de aproximación antes de programar el cierre de la pinza.

Comprender el orden correcto de las operaciones ayudará a evitar errores cuando comiencen a desarrollar secuencias automáticas de manipulación.

:::

---

## Preparando el control desde Python

En el siguiente apartado aprenderemos a controlar la pinza directamente desde Python.

Programaremos su apertura y cierre, sincronizándola con los movimientos del UR3 para construir nuestro primer ciclo completo de **pick & place**.

A partir de ese momento, el robot será capaz de recoger y depositar piezas de forma completamente automática.

---

## 20.3 Controlando la pinza desde Python

Una vez que el UR3 ha llegado correctamente hasta la pieza, es necesario sujetarla.

Para ello utilizaremos la **pinza paralela**, controlando su apertura y cierre desde Python.

En una instalación industrial real, este control suele realizarse mediante señales digitales, protocolos de comunicación industriales o controladores específicos.

En CoppeliaSim el proceso resulta mucho más sencillo y nos permitirá concentrarnos en la lógica de la aplicación.

---

### Localizando la pinza

Al igual que ocurría con las articulaciones o con `UR3_target`, la pinza debe disponer de su propio identificador (*handle*).

En el árbol real del UR3 utilizado en estas prácticas no aparece una pinza llamada `Gripper` dentro de `/UR3`. El modelo base termina en la zona de `connection` y `link7_visible`. Por tanto, antes de programarla debemos añadir la herramienta a la escena, acoplarla al extremo del robot y asignarle un nombre claro.

Durante este capítulo utilizaremos el nombre:

```text
UR3_gripper
```

El primer paso consistirá en obtener dicho identificador para poder acceder a ella desde nuestro programa.

```python
gripper = sim.getObject('/UR3_gripper')
```

A partir de este momento podremos enviar órdenes para controlar su funcionamiento.

Si tu pinza tiene otro nombre en el árbol de la escena, sustituye `/UR3_gripper` por la ruta real. Lo importante es no utilizar `/UR3/Gripper` salvo que ese objeto exista realmente en tu escena.

::: figure
image: ../assets/cap20/fig20_5.png
caption: Obtención del *handle* de la pinza del UR3 desde Python.
:::

---

## Abrir la pinza

Antes de aproximarnos a una pieza, la pinza debe encontrarse abierta.

En una simulación esto significa que los dos dedos estarán separados la distancia suficiente para permitir la entrada del objeto.

La apertura deberá realizarse siempre antes del descenso del robot.

De esta forma evitaremos colisiones innecesarias.

---

## Cerrar la pinza

Cuando el efector final alcanza la posición correcta, llega el momento de sujetar la pieza.

El cierre de la pinza debe producirse únicamente cuando el robot ya se encuentra completamente detenido.

Una vez cerrada, la pieza podrá desplazarse junto con el efector final durante toda la operación de transporte.

::: figure
image: ../assets/cap20/fig20_6.png
caption: Apertura y cierre de la pinza sincronizados con el movimiento del UR3.
:::

---

### Una secuencia sincronizada

La coordinación entre el robot y la pinza puede representarse mediante la siguiente secuencia:

```text
Mover sobre la pieza
        │
        ▼
Descender
        │
        ▼
Cerrar pinza
        │
        ▼
Esperar
        │
        ▼
Elevar la pieza
```

Observa que existe una pequeña pausa entre el cierre de la pinza y la elevación.

Aunque en la simulación el movimiento sea prácticamente instantáneo, esta espera mejora la estabilidad y reproduce el comportamiento habitual de un robot industrial.

---

### Buenas prácticas

Cuando programes operaciones de manipulación procura seguir siempre estas recomendaciones:

- Abre la pinza antes de aproximarte a la pieza.
- Cierra la pinza únicamente cuando el robot esté detenido.
- Eleva la pieza unos centímetros antes de iniciar el desplazamiento horizontal.
- Deposita la pieza completamente antes de abrir la pinza.
- Retira el robot verticalmente antes de abandonar la zona de trabajo.

Estas pequeñas precauciones reducen el riesgo de colisiones y facilitan enormemente la programación de trayectorias seguras.

::: teacher
content:

Durante las primeras prácticas es recomendable ejecutar la simulación a velocidad reducida.

De este modo el alumnado podrá observar claramente la coordinación entre el movimiento del UR3 y el accionamiento de la pinza, comprendiendo la importancia de sincronizar correctamente ambas acciones.

:::

---

## Preparando el primer ciclo completo

Ya disponemos de todos los elementos necesarios para desarrollar una operación completa de manipulación.

En el siguiente apartado integraremos el movimiento de `UR3_target` con la apertura y el cierre de la pinza para construir nuestro primer programa completo de **pick & place** utilizando el **UR3** y Python.

---

## 20.4 Nuestro primer programa *Pick & Place*

Ha llegado el momento de integrar todos los conocimientos adquiridos durante este capítulo.

Hasta ahora hemos aprendido a:

- mover `UR3_target` mediante coordenadas cartesianas;
- controlar la apertura y el cierre de la pinza;
- utilizar posiciones de aproximación;
- sincronizar el movimiento del robot con el accionamiento del efector final.

Ahora construiremos una secuencia completa capaz de recoger una pieza y depositarla en una nueva posición.

---

### Definiendo las posiciones de trabajo

Antes de escribir el programa es recomendable definir todas las posiciones que utilizará el robot.

En nuestro ejemplo emplearemos cuatro posiciones principales.

```python
APROX_ORIGEN = [0.35, -0.15, 0.30]
RECOGIDA     = [0.35, -0.15, 0.20]

APROX_DESTINO = [0.10, 0.20, 0.30]
DEPOSITO      = [0.10, 0.20, 0.20]
```

Observa que cada punto de recogida o depósito tiene asociada una posición de aproximación situada unos centímetros por encima.

Este procedimiento será una constante durante todo el libro.

::: figure
image: ../assets/cap20/fig20_7.png
caption: Posiciones utilizadas durante una operación completa de *pick & place*.
:::

---

## La secuencia completa

Una vez definidas las posiciones, la lógica del programa resulta muy sencilla.

```python
abrir_pinza()

mover_target(APROX_ORIGEN)
mover_target(RECOGIDA)

cerrar_pinza()

mover_target(APROX_ORIGEN)

mover_target(APROX_DESTINO)
mover_target(DEPOSITO)

abrir_pinza()

mover_target(APROX_DESTINO)
```

Aunque el programa contiene pocas instrucciones, el UR3 ejecutará una operación completa de manipulación.

Cada función representa una tarea de alto nivel que reutilizaremos constantemente en los siguientes capítulos.

---

### Analizando el ciclo

Si observamos detenidamente el programa, veremos que puede dividirse en ocho etapas perfectamente diferenciadas.

1. Abrir la pinza.
2. Aproximarse a la pieza.
3. Descender hasta la posición de recogida.
4. Sujetar la pieza.
5. Elevar la carga.
6. Desplazarse hasta el destino.
7. Depositar la pieza.
8. Regresar a una posición segura.

Esta organización facilita la lectura del código y simplifica enormemente las futuras modificaciones.

::: figure
image: ../assets/cap20/fig20_8.png
caption: Secuencia completa del primer programa de *pick & place* desarrollado con el UR3.
:::

---

## ¿Por qué dividir el movimiento en fases?

En aplicaciones industriales rara vez se escribe un único programa largo.

Lo habitual consiste en dividir el comportamiento del robot en pequeñas operaciones reutilizables.

Por ejemplo:

- mover hasta una posición;
- abrir la pinza;
- cerrar la pinza;
- esperar una confirmación;
- regresar a una posición segura.

Esta forma de trabajar presenta numerosas ventajas.

- El código resulta más fácil de leer.
- Es más sencillo localizar errores.
- Permite reutilizar funciones en diferentes programas.
- Facilita el mantenimiento de la aplicación.

En los próximos capítulos seguiremos este mismo criterio para construir aplicaciones cada vez más complejas.

::: teacher
content:

Anima al alumnado a ejecutar el programa paso a paso.

Después de cada movimiento, pide que identifiquen en qué fase del ciclo se encuentra el robot.

Este ejercicio ayuda a comprender la lógica de una aplicación industrial y prepara el terreno para introducir máquinas de estados en capítulos posteriores.

:::

---

## Hacia aplicaciones industriales reales

Aunque nuestro ejemplo únicamente manipula una pieza, la estructura del programa es prácticamente idéntica a la utilizada en muchas estaciones robotizadas reales.

La diferencia es que, en una instalación industrial, las posiciones suelen obtenerse mediante sensores, cámaras de visión artificial o sistemas de calibración automática.

En el próximo apartado aprenderemos a repetir este ciclo de forma automática para construir una secuencia continua de manipulación, tal como ocurre en una línea de producción.

---

## 20.5 Automatizando el ciclo de manipulación

Hasta ahora nuestro programa ha ejecutado una única operación de **pick & place**.

Sin embargo, en una instalación industrial real el robot no trabaja una sola vez.

Su misión consiste en repetir la misma operación cientos o incluso miles de veces con la máxima precisión.

Por este motivo, transformaremos nuestro programa en un **ciclo automático**, capaz de ejecutar continuamente la misma secuencia de manipulación.

---

### Reutilizando la secuencia

Una buena práctica consiste en agrupar todas las operaciones de recogida y depósito dentro de una única función.

Por ejemplo:

```python
def pick_and_place():

    abrir_pinza()

    mover_target(APROX_ORIGEN)
    mover_target(RECOGIDA)

    cerrar_pinza()

    mover_target(APROX_ORIGEN)

    mover_target(APROX_DESTINO)
    mover_target(DEPOSITO)

    abrir_pinza()

    mover_target(APROX_DESTINO)
```

Esta función representa un ciclo completo de trabajo del UR3.

Cada vez que la ejecutemos, el robot recogerá una pieza y la depositará en su posición de destino.

::: figure
image: ../assets/cap20/fig20_9.png
caption: Organización del ciclo completo de manipulación dentro de una función reutilizable.
:::

---

## Repitiendo el proceso

Una vez creada la función, automatizar el proceso resulta muy sencillo.

Basta con ejecutarla repetidamente.

```python
while True:

    pick_and_place()
```

Con estas dos líneas el robot continuará trabajando mientras la simulación permanezca activa.

Este tipo de programación es muy habitual en aplicaciones industriales donde el robot permanece funcionando durante toda la jornada.

---

### ¿Cómo se detiene el robot?

En una fábrica real el robot no trabaja indefinidamente.

El ciclo suele detenerse cuando ocurre alguna de las siguientes situaciones:

- no quedan piezas por manipular;
- un sensor detecta una incidencia;
- el operario pulsa el botón de parada;
- finaliza la orden de fabricación;
- aparece una alarma de seguridad.

En nuestros primeros programas utilizaremos un ciclo continuo para simplificar el aprendizaje.

Más adelante aprenderemos a controlar estas situaciones mediante sensores y condiciones de parada.

::: figure
image: ../assets/cap20/fig20_10.png
caption: Ejecución repetitiva del ciclo de manipulación hasta recibir una condición de parada.
:::

---

## Programando como en la industria

Si observamos el código, veremos que comienza a parecerse al utilizado en aplicaciones industriales reales.

En lugar de escribir largas secuencias de instrucciones, organizamos el programa en pequeñas funciones claramente diferenciadas.

Por ejemplo:

- mover el robot;
- abrir la pinza;
- cerrar la pinza;
- ejecutar un ciclo completo;
- repetir el proceso.

Esta forma de trabajar presenta numerosas ventajas.

- El programa resulta más fácil de mantener.
- Las funciones pueden reutilizarse en otros proyectos.
- La lectura del código es mucho más clara.
- Es sencillo localizar y corregir errores.

En los siguientes capítulos seguiremos ampliando esta estructura hasta construir una aplicación robotizada completa.

---

### Hacia una célula robotizada

Hasta ahora el UR3 ha trabajado siempre con una única pieza situada en una posición fija.

En una célula robotizada real esto rara vez ocurre.

Las piezas llegan continuamente mediante una cinta transportadora, son detectadas por sensores y clasificadas automáticamente antes de ser manipuladas.

En el próximo capítulo construiremos una célula completa donde el UR3 colaborará con sensores y otros elementos de automatización para realizar un proceso industrial continuo.

::: teacher
content:

Antes de pasar al siguiente capítulo, propone al alumnado modificar las posiciones de recogida y depósito.

De este modo comprobarán que el mismo programa puede reutilizarse para manipular piezas situadas en diferentes lugares simplemente cambiando las coordenadas de trabajo, sin necesidad de modificar la lógica del ciclo.

:::

---

## 20.6 Práctica guiada: Construcción de una operación completa de *Pick & Place*

En esta práctica desarrollarás una aplicación completa de manipulación utilizando el **UR3**, una pinza paralela y las técnicas de programación aprendidas a lo largo del capítulo.

El objetivo consiste en construir un ciclo automático capaz de recoger una pieza, transportarla y depositarla en otra posición de forma repetitiva.

::: practice
title: Primer ciclo automático de manipulación

difficulty: Media

time: 75 minutos

content:

Realiza las siguientes actividades:

1. Abre la escena del UR3 utilizada durante este capítulo.
2. Comprueba que la pinza responde correctamente a las órdenes de apertura y cierre.
3. Define las posiciones de aproximación y recogida.
4. Define las posiciones de aproximación y depósito.
5. Programa la función `pick_and_place()`.
6. Ejecuta un ciclo completo comprobando cada fase del movimiento.
7. Convierte el programa en un ciclo continuo utilizando un bucle.
8. Modifica las coordenadas de destino para comprobar que el mismo programa puede reutilizarse.
9. Repite la operación con diferentes posiciones de recogida.
10. Verifica que el robot mantiene siempre una trayectoria segura.

Al finalizar la práctica deberás ser capaz de desarrollar una aplicación básica de manipulación utilizando el UR3 y Python.

:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Efector final | Herramienta situada en el extremo del brazo robótico. |
| Pinza paralela | Efector final formado por dos dedos que sujetan una pieza. |
| Pick & Place | Operación consistente en recoger una pieza y depositarla en otra posición. |
| Aproximación | Posición situada por encima de la pieza que permite acceder de forma segura. |
| Recogida | Fase en la que la pinza sujeta la pieza. |
| Transporte | Movimiento del robot con la pieza ya capturada. |
| Depósito | Liberación controlada de la pieza en el punto de destino. |
| Ciclo automático | Repetición continua de una secuencia de manipulación. |
| Función reutilizable | Bloque de código diseñado para ejecutarse múltiples veces. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender el funcionamiento de una operación **Pick & Place**.
- ✅ Identificar las fases de una manipulación industrial.
- ✅ Controlar una pinza paralela desde Python.
- ✅ Coordinar el movimiento del UR3 con la apertura y el cierre de la pinza.
- ✅ Programar trayectorias seguras mediante posiciones de aproximación.
- ✅ Construir un programa completo de manipulación.
- ✅ Automatizar el ciclo mediante funciones reutilizables.

A partir de este momento ya puedes desarrollar pequeñas aplicaciones de manipulación utilizando el **UR3**.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué significa la expresión **Pick & Place**?
2. ¿Por qué se utilizan posiciones de aproximación?
3. ¿Cuándo debe cerrarse la pinza durante una operación de manipulación?
4. ¿Qué ventajas ofrece dividir el programa en funciones reutilizables?
5. ¿Por qué conviene elevar la pieza antes del desplazamiento horizontal?
6. ¿Qué beneficios aporta un ciclo automático frente a una ejecución única?
7. ¿Qué modificaciones serían necesarias para manipular piezas situadas en distintas posiciones?

Si puedes responder correctamente a todas ellas, estás preparado para abordar una aplicación robotizada completa.

---

## Reto

::: challenge
title: Manipulación de varias piezas

content:

Amplía el programa desarrollado durante este capítulo para que el UR3 manipule tres piezas situadas en posiciones diferentes.

Para ello deberás:

- definir varias posiciones de recogida;
- utilizar una misma posición de depósito;
- reutilizar la función `pick_and_place()`;
- comprobar que el robot mantiene trayectorias seguras durante todo el proceso.

Como ampliación, modifica el programa para que la posición de destino cambie automáticamente después de cada pieza.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Consolidar el control cartesiano del UR3.
- Coordinar correctamente el movimiento del robot con la pinza.
- Introducir la programación modular mediante funciones.
- Preparar al alumnado para el desarrollo de una célula robotizada completa.

**Material necesario**

- Ordenadores con CoppeliaSim y Python.
- Escena del UR3 utilizada durante la Parte IV.
- Pinza paralela configurada en la simulación.

**Consejos metodológicos**

Es recomendable que el alumnado ejecute inicialmente el ciclo paso a paso.

Una vez comprendida la secuencia, puede automatizarse mediante un bucle continuo y, posteriormente, modificarse para manipular varias piezas cambiando únicamente las coordenadas de trabajo.

:::

---

## Próximo capítulo

Hasta ahora el **UR3** ha trabajado de forma aislada.

En el siguiente capítulo construiremos una **célula robotizada completa**, incorporando una cinta transportadora, sensores de presencia y un sistema de clasificación de piezas.

El robot dejará de ejecutar movimientos predefinidos para integrarse en un proceso automático similar al de una instalación industrial real.

Este proyecto reunirá todos los conocimientos adquiridos desde el comienzo de la Parte IV y servirá como cierre del bloque dedicado a la **robótica industrial y manipulación**.
