::: chapter-cover
number: 11
title: Programación estructurada del Pioneer P3DX
time: 5 horas
level: ⭐⭐⭐⭐☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo

content:

Al finalizar este capítulo serás capaz de:

- Comprender la importancia de escribir programas estructurados y fáciles de mantener.
- Dividir un programa de robótica en funciones reutilizables.
- Separar la configuración del robot de la lógica de control.
- Organizar correctamente un proyecto en Python.
- Desarrollar un programa completo para el Pioneer P3DX siguiendo buenas prácticas de programación.

:::

# Capítulo 11 · Programación estructurada del Pioneer P3DX

### De programas de prueba a aplicaciones reales

En los capítulos anteriores hemos desarrollado diferentes programas para controlar el Pioneer P3DX.

Cada uno de ellos tenía un objetivo concreto: leer un sensor, mover los motores o evitar obstáculos.

Estos programas han resultado muy útiles para aprender los fundamentos de la programación de robots móviles.

Sin embargo, presentan un inconveniente importante.

A medida que un programa crece, también aumenta su complejidad.

Si todo el código se escribe de forma continua dentro del programa principal, pronto se vuelve difícil de leer, modificar y mantener.

Esta situación recibe habitualmente el nombre de **código monolítico**.

En proyectos pequeños puede parecer suficiente, pero en aplicaciones reales termina convirtiéndose en un problema.

Los programas utilizados en robótica industrial suelen contener miles o incluso decenas de miles de líneas de código.

Sin una organización adecuada sería prácticamente imposible comprender su funcionamiento o introducir nuevas funcionalidades sin provocar errores.

Por este motivo resulta imprescindible aprender a estructurar correctamente un programa.

En este capítulo transformaremos el algoritmo desarrollado en el capítulo anterior en una aplicación organizada, modular y fácil de ampliar.

El comportamiento del robot será exactamente el mismo.

Lo que cambiará será la forma de construir el programa.

Nuestro objetivo será escribir menos código repetido, facilitar su mantenimiento y preparar el proyecto para incorporar nuevas funcionalidades en capítulos posteriores.

::: teacher
title: Consejo para el profesor

content:

Antes de comenzar este capítulo, muestra al alumnado un programa muy largo escrito completamente dentro del bloque principal y pregúntales cuánto tardarían en localizar un error concreto.

A continuación presenta el mismo programa dividido en funciones.

La comparación permite comprender rápidamente la utilidad de la programación estructurada.

:::

---

## 11.1 ¿Por qué organizar mejor nuestros programas?

Observa el siguiente fragmento de código.

Aunque funciona correctamente, mezcla en un mismo bloque tareas muy diferentes.

- Inicializa la conexión con CoppeliaSim.
- Obtiene las referencias al robot.
- Lee los sensores.
- Controla los motores.
- Decide el movimiento.
- Gestiona el bucle principal.

Cuando todas estas responsabilidades aparecen mezcladas, el programa resulta difícil de comprender.

Además, cualquier modificación obliga a revisar una gran cantidad de código.

Una solución mucho más adecuada consiste en dividir el programa en pequeños bloques independientes.

::: figure
image: ../assets/cap11/generated/programa_monolitico_vs_estructurado.png
caption: Comparación entre un programa monolítico y un programa estructurado. Dividir el código en funciones con responsabilidades bien definidas facilita su lectura, mantenimiento y ampliación.
:::

Cada bloque será responsable de realizar una única tarea.

Por ejemplo:

- conectar con CoppeliaSim;
- obtener las referencias del robot;
- leer los sensores;
- controlar los motores;
- decidir el movimiento;
- ejecutar el bucle principal.

Esta forma de trabajar recibe el nombre de **programación estructurada**.

Gracias a ella los programas resultan mucho más sencillos de leer, depurar y ampliar.

En los siguientes apartados aprenderemos a transformar nuestro algoritmo de navegación autónoma siguiendo esta filosofía.

::: info
title: Una idea muy importante

content:

Un programa bien estructurado no necesariamente hace más cosas que otro.

La diferencia es que resulta mucho más fácil de comprender, mantener y ampliar.

En proyectos profesionales esta característica es incluso más importante que escribir el menor número posible de líneas de código.

:::

---

::: summary
title: Idea clave

content:

La calidad de un programa no depende únicamente de que funcione correctamente.

También debe ser fácil de leer, modificar y mantener.

La programación estructurada permite dividir un problema complejo en pequeñas tareas independientes, facilitando el desarrollo de aplicaciones de robótica cada vez más avanzadas.

:::

---

## 11.2 Creando funciones reutilizables

En el apartado anterior hemos comprobado que un programa resulta mucho más fácil de comprender cuando cada parte del código tiene una responsabilidad bien definida.

La herramienta que nos permite conseguir este objetivo en Python son las **funciones**.

Una función es un bloque de código que realiza una tarea concreta y que puede utilizarse tantas veces como sea necesario sin necesidad de volver a escribir las mismas instrucciones.

Gracias a ellas conseguimos programas más claros, más cortos y mucho más fáciles de mantener.

::: figure
image: ../assets/cap11/generated/division_programa_funciones.png
caption: División de un programa en funciones reutilizables. El programa principal coordina la ejecución mientras cada función realiza una tarea específica, facilitando la reutilización, el mantenimiento y la ampliación del código.
:::

---

### ¿Qué es una función?

Podemos imaginar una función como una pequeña máquina especializada.

Cada vez que la llamamos, realiza una tarea determinada y, cuando termina, devuelve el control al programa principal.

Por ejemplo, en lugar de escribir continuamente las instrucciones necesarias para detener el robot, podemos agruparlas dentro de una función.

```python
def detener_robot():

    sim.setJointTargetVelocity(motor_izquierdo, 0)

    sim.setJointTargetVelocity(motor_derecho, 0)
```

A partir de ese momento bastará con escribir:

```python
detener_robot()
```

El resultado será exactamente el mismo, pero el programa será mucho más sencillo de leer.

---

### Creando nuestra primera función

Supongamos que queremos avanzar siempre con la misma velocidad.

En lugar de repetir las mismas instrucciones varias veces, podemos encapsularlas en una función.

```python
def avanzar():

    sim.setJointTargetVelocity(motor_izquierdo, VELOCIDAD)

    sim.setJointTargetVelocity(motor_derecho, VELOCIDAD)
```

Ahora el programa principal queda reducido a una única línea.

```python
avanzar()
```

La intención del código resulta mucho más evidente.

No necesitamos leer las instrucciones internas para comprender qué está haciendo el robot.

---

### Funciones con parámetros

En muchas ocasiones necesitaremos que una misma función pueda realizar pequeñas variaciones de una misma tarea.

Para ello utilizaremos **parámetros**.

Por ejemplo, podemos crear una función capaz de controlar ambos motores indicando la velocidad de cada uno.

```python
def mover_robot(velocidad_izquierda, velocidad_derecha):

    sim.setJointTargetVelocity(motor_izquierdo, velocidad_izquierda)

    sim.setJointTargetVelocity(motor_derecho, velocidad_derecha)
```

Ahora podremos utilizar la misma función para cualquier movimiento.

```python
mover_robot(2.0, 2.0)
```

Avanzar.

```python
mover_robot(-2.0, -2.0)
```

Retroceder.

```python
mover_robot(2.0, -2.0)
```

Girar sobre el eje.

Una única función permite controlar todos los movimientos del Pioneer P3DX.

---

### Funciones que devuelven información

Las funciones no solo ejecutan acciones.

También pueden devolver información al programa.

Por ejemplo, podemos crear una función que lea el sensor frontal y devuelva únicamente si existe o no un obstáculo.

```python
def obstaculo_detectado():

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    return resultado
```

Gracias a esta función el programa principal resulta mucho más expresivo.

```python
if obstaculo_detectado():

    detener_robot()

else:

    avanzar()
```

Observa cómo ahora el código se parece mucho más al algoritmo que diseñamos en el capítulo anterior.

---

### Ventajas de utilizar funciones

Dividir un programa en funciones aporta numerosas ventajas.

- Evita repetir código.
- Facilita la lectura del programa.
- Reduce la aparición de errores.
- Simplifica las tareas de mantenimiento.
- Permite reutilizar el mismo código en diferentes proyectos.

Estas ventajas hacen que prácticamente todas las aplicaciones profesionales utilicen esta forma de organización.

::: info
title: Una buena práctica

content:

Cada función debería realizar una única tarea.

Si una función comienza a hacer demasiadas cosas diferentes, probablemente ha llegado el momento de dividirla en varias funciones más pequeñas.

Este principio facilita enormemente el mantenimiento del programa.

:::

---

::: summary
title: Idea clave

content:

Las funciones permiten dividir un programa en pequeñas tareas independientes.

Gracias a ellas el código resulta más claro, reutilizable y fácil de mantener, convirtiéndose en una herramienta imprescindible para desarrollar aplicaciones de robótica de calidad.

:::

---

## 11.3 Separando la configuración de la lógica del programa

En el apartado anterior hemos aprendido a dividir nuestro programa en funciones.

Sin embargo, todavía existe un aspecto que podemos mejorar.

Observa el siguiente ejemplo.

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)
```

¿Qué ocurriría si más adelante decidimos que el robot debe avanzar más despacio?

Tendríamos que localizar todas las líneas donde aparece el valor `2.0` y sustituirlo manualmente.

Además de resultar incómodo, este procedimiento aumenta la probabilidad de cometer errores.

Una solución mucho más profesional consiste en almacenar todos los parámetros de configuración en un único lugar del programa.

::: figure
image: ../assets/cap11/generated/organizacion_programa_robotica.png
caption: Organización recomendada de un programa de robótica. Separar la configuración, las funciones y el programa principal facilita la lectura del código, simplifica su mantenimiento y permite ampliar la aplicación de forma ordenada.
:::

---

### Definiendo constantes

En Python es habitual declarar al comienzo del programa todas aquellas variables cuyo valor permanecerá constante durante la ejecución.

Por ejemplo:

```python
VELOCIDAD_AVANCE = 2.0
VELOCIDAD_GIRO = 2.0
TIEMPO_GIRO = 0.8
TIEMPO_PARADA = 0.2
```

A partir de ese momento utilizaremos estas constantes en lugar de escribir directamente los valores numéricos.

```python
mover_robot(
    VELOCIDAD_AVANCE,
    VELOCIDAD_AVANCE
)
```

Si en el futuro queremos modificar la velocidad de avance, únicamente tendremos que cambiar el valor de la constante.

---

### Ventajas de utilizar constantes

Separar la configuración del resto del programa aporta numerosas ventajas.

- Todos los parámetros se encuentran agrupados.
- Las modificaciones resultan mucho más sencillas.
- El código es más fácil de leer.
- Se evitan errores provocados por valores repetidos.
- El programa resulta más flexible y reutilizable.

Este tipo de organización es muy habitual en aplicaciones industriales y proyectos de robótica de gran tamaño.

---

### Un ejemplo práctico

Compara los dos fragmentos siguientes.

Código sin constantes:

```python
mover_robot(2.0, 2.0)

time.sleep(0.2)

mover_robot(2.0, -2.0)

time.sleep(0.8)
```

Código utilizando constantes:

```python
mover_robot(
    VELOCIDAD_AVANCE,
    VELOCIDAD_AVANCE
)

time.sleep(TIEMPO_PARADA)

mover_robot(
    VELOCIDAD_GIRO,
    -VELOCIDAD_GIRO
)

time.sleep(TIEMPO_GIRO)
```

Aunque ambos programas realizan exactamente las mismas acciones, el segundo resulta mucho más expresivo.

El lector comprende inmediatamente qué representa cada valor sin necesidad de analizar el resto del código.

---

### Organizando el inicio del programa

Una buena práctica consiste en comenzar todos los programas con una sección claramente diferenciada donde aparezcan las constantes de configuración.

Por ejemplo:

```python
# ------------------------------------
# Configuración
# ------------------------------------

VELOCIDAD_AVANCE = 2.0
VELOCIDAD_GIRO = 2.0

TIEMPO_PARADA = 0.2
TIEMPO_GIRO = 0.8
```

A continuación pueden definirse las funciones y, finalmente, el programa principal.

Esta organización facilita enormemente la lectura del código y permite localizar rápidamente cualquier parámetro que sea necesario modificar.

::: info
title: Una recomendación profesional

content:

Evita escribir números "mágicos" directamente dentro del código.

Siempre que un valor tenga un significado concreto, conviene almacenarlo en una constante con un nombre descriptivo.

Esta práctica mejora considerablemente la claridad y el mantenimiento del programa.

:::

---

::: summary
title: Idea clave

content:

Separar la configuración del resto de la lógica permite construir programas más claros, fáciles de modificar y preparados para crecer sin perder legibilidad.

Las constantes constituyen una herramienta sencilla pero fundamental para desarrollar aplicaciones profesionales de robótica.

:::

---

## 11.4 Construyendo un programa profesional

Ya conocemos los elementos necesarios para desarrollar una aplicación de robótica bien organizada.

Hemos aprendido a dividir el código en funciones y a separar la configuración del comportamiento del robot.

Ha llegado el momento de unir todas estas ideas en un único programa.

Nuestro objetivo será construir una estructura que pueda crecer fácilmente conforme incorporemos nuevas funcionalidades.

Aunque el ejemplo sigue siendo sencillo, la organización utilizada es muy similar a la empleada en aplicaciones profesionales.

::: figure
image: ../assets/cap11/generated/estructura_aplicacion_robotica_python.png
caption: Estructura recomendada de una aplicación de robótica desarrollada en Python. La configuración, las funciones y el programa principal se organizan en bloques independientes que facilitan la comprensión, el mantenimiento y la ampliación del código.
:::

---

### La estructura general

A partir de este capítulo todos nuestros programas seguirán prácticamente el mismo esquema.

```text
Configuración

↓

Funciones

↓

Programa principal (main)

↓

Inicio de la ejecución
```

Cada una de estas partes tiene una responsabilidad claramente definida.

La configuración almacena todos los parámetros modificables.

Las funciones implementan las diferentes tareas del programa.

Finalmente, el programa principal coordina toda la ejecución.

---

### La sección de configuración

Comenzaremos declarando todas las constantes del programa.

```python
VELOCIDAD_AVANCE = 2.0
VELOCIDAD_GIRO = 2.0

TIEMPO_PARADA = 0.2
TIEMPO_GIRO = 0.8
```

Agrupar todos estos valores facilita enormemente futuras modificaciones.

---

### Definiendo las funciones

A continuación declararemos las funciones que utilizará el programa.

Por ejemplo:

```python
def mover_robot(v_izquierda, v_derecha):

    sim.setJointTargetVelocity(
        motor_izquierdo,
        v_izquierda
    )

    sim.setJointTargetVelocity(
        motor_derecho,
        v_derecha
    )
```

O la función encargada de comprobar si existe un obstáculo.

```python
def obstaculo_detectado():

    resultado, distancia, punto, objeto, normal = \
        sim.readProximitySensor(sensor)

    return resultado
```

Observa que cada función realiza una única tarea.

Esto facilita enormemente la lectura del programa.

---

### El programa principal

Toda la lógica de control queda concentrada dentro de una única función.

```python
def main():

    while True:

        if obstaculo_detectado():

            mover_robot(
                VELOCIDAD_GIRO,
                -VELOCIDAD_GIRO
            )

        else:

            mover_robot(
                VELOCIDAD_AVANCE,
                VELOCIDAD_AVANCE
            )
```

Gracias a esta organización, el programa resulta muy fácil de comprender.

Incluso sin conocer el contenido de cada función podemos seguir perfectamente el comportamiento del robot.

---

### Iniciando la aplicación

Finalmente solo queda ejecutar el programa principal.

```python
if __name__ == "__main__":

    main()
```

Esta construcción es muy habitual en Python.

Permite que el programa comience su ejecución únicamente cuando el archivo se ejecuta directamente.

Además, facilita reutilizar las funciones desde otros módulos en proyectos de mayor tamaño.

::: info
title: ¿Por qué utilizamos main()?

content:

La función `main()` actúa como punto de entrada de la aplicación.

Toda la lógica principal queda concentrada en un único lugar, mientras que el resto del código se organiza en funciones auxiliares.

Esta estructura mejora notablemente la claridad del programa y facilita su mantenimiento.

:::

---

### Ventajas de esta organización

A partir de ahora nuestros programas presentarán numerosas ventajas.

- Son más fáciles de leer.
- Resultan más sencillos de depurar.
- Permiten añadir nuevas funciones sin modificar el resto del código.
- Facilitan el trabajo colaborativo.
- Se aproximan a la estructura utilizada en proyectos profesionales.

En realidad, esta forma de organizar el código es independiente de CoppeliaSim.

Podrás utilizarla en prácticamente cualquier proyecto desarrollado en Python.

::: summary
title: Idea clave

content:

Una aplicación profesional no solo debe funcionar correctamente.

También debe estar organizada de forma que cualquier persona pueda comprenderla, modificarla y ampliarla con facilidad.

La combinación de constantes, funciones y un programa principal constituye una excelente base para desarrollar aplicaciones de robótica de calidad.

:::

---

## 11.5 Proyecto final · Un robot móvil organizado y fácil de mantener

Ha llegado el momento de aplicar todos los conocimientos adquiridos a lo largo de esta segunda parte del libro.

Durante los capítulos anteriores hemos aprendido a:

- conocer el Pioneer P3DX;
- utilizar sus sensores de proximidad;
- controlar el movimiento mediante los motores;
- desarrollar un algoritmo capaz de evitar obstáculos;
- organizar correctamente un programa utilizando funciones y constantes.

Ahora reuniremos todas estas ideas en un único proyecto.

Nuestro objetivo no será crear un algoritmo más complejo, sino construir una aplicación bien organizada que sirva como base para futuros desarrollos.

---

### La estructura del proyecto

El programa seguirá siempre el mismo orden.

```text
Configuración

↓

Variables globales

↓

Funciones

↓

Programa principal

↓

Inicio de la aplicación
```

Gracias a esta organización cualquier persona podrá localizar rápidamente cada parte del código.

---

### Paso 1. Configuración

Comenzaremos definiendo todos los parámetros modificables.

```python
VELOCIDAD_AVANCE = 2.0
VELOCIDAD_GIRO = 2.0

TIEMPO_PARADA = 0.2
TIEMPO_GIRO = 0.8
```

En un proyecto real podrían existir decenas de parámetros.

Agruparlos facilita enormemente el mantenimiento.

---

### Paso 2. Variables globales

A continuación almacenaremos las referencias a los objetos del robot.

```python
sensor = None

motor_izquierdo = None

motor_derecho = None
```

Estas variables serán inicializadas durante la conexión con CoppeliaSim y posteriormente utilizadas por todas las funciones del programa.

---

### Paso 3. Funciones

Después declararemos todas las funciones necesarias.

Por ejemplo:

- conectar();
- obtener_referencias();
- mover_robot();
- detener_robot();
- obstaculo_detectado();
- main().

Cada una tendrá una única responsabilidad.

---

### Paso 4. Programa principal

Finalmente ejecutaremos el algoritmo de navegación.

```python
def main():

    while True:

        if obstaculo_detectado():

            detener_robot()

            girar()

        else:

            avanzar()
```

Observa que el programa principal apenas contiene unas pocas líneas.

Toda la complejidad se encuentra distribuida entre funciones especializadas.

Esta es precisamente la principal ventaja de la programación estructurada.

---

### Un programa preparado para crecer

A partir de esta organización resultará muy sencillo incorporar nuevas funcionalidades.

Por ejemplo:

- utilizar varios sensores;
- controlar la velocidad en función de la distancia al obstáculo;
- añadir nuevos comportamientos;
- incorporar una cámara;
- utilizar visión artificial;
- integrar ROS 2.

Todas estas mejoras podrán desarrollarse sin modificar la estructura general del programa.

Únicamente será necesario añadir nuevas funciones o ampliar las ya existentes.

::: info
title: La programación profesional

content:

Los programas desarrollados en empresas de robótica pueden contener decenas de miles de líneas de código.

Sin una organización adecuada sería prácticamente imposible mantenerlos.

La programación estructurada constituye el primer paso para construir aplicaciones robustas, reutilizables y fáciles de ampliar.

:::

---

::: challenge
title: Proyecto de ampliación

difficulty: Alta

content:

Reestructura todos los programas desarrollados en los capítulos 8, 9 y 10 siguiendo la organización aprendida en este capítulo.

Intenta que todos ellos compartan la misma estructura:

- configuración;
- funciones;
- programa principal.

Comprobarás que el código resulta mucho más sencillo de mantener y que añadir nuevas funcionalidades requiere un esfuerzo mucho menor.

:::

---

::: summary
title: Idea clave

content:

La calidad de un programa no depende únicamente de que funcione.

También debe ser claro, modular y fácil de ampliar.

La programación estructurada permite construir aplicaciones de robótica preparadas para crecer conforme aumente la complejidad del proyecto.

:::

::: figure
image: ../assets/cap11/generated/evolucion_proyecto_robotica.png
caption: Evolución del aprendizaje a lo largo de la Parte II. Desde el conocimiento del Pioneer P3DX hasta el desarrollo de aplicaciones de robótica estructuradas y profesionales, integrando percepción, movimiento, toma de decisiones y buenas prácticas de programación.
:::

---

# Conceptos clave

Al finalizar este capítulo deberías recordar las siguientes ideas fundamentales.

- La programación estructurada divide un programa complejo en pequeñas tareas independientes.
- Cada función debe tener una única responsabilidad.
- Las funciones permiten reutilizar código y evitar repeticiones innecesarias.
- Las constantes facilitan la modificación de parámetros sin alterar la lógica del programa.
- Separar la configuración, las funciones y el programa principal mejora la claridad del código.
- La función `main()` coordina la ejecución de la aplicación.
- Una buena organización facilita la depuración, el mantenimiento y la ampliación del programa.
- La estructura utilizada en este capítulo constituye la base de aplicaciones profesionales de robótica desarrolladas en Python.

---

# Autoevaluación

Responde a las siguientes preguntas antes de continuar con la siguiente parte del libro.

1. ¿Qué ventajas ofrece la programación estructurada frente a un programa monolítico?

2. ¿Cuál es la función principal de una función en Python?

3. ¿Por qué es recomendable que cada función tenga una única responsabilidad?

4. ¿Qué ventajas aporta utilizar constantes en lugar de escribir directamente valores numéricos?

5. ¿Qué misión desempeña la función `main()` dentro de una aplicación?

6. ¿Por qué conviene separar la configuración del comportamiento del robot?

7. ¿Qué ventajas ofrece reutilizar funciones en diferentes proyectos?

8. ¿Cómo organizarías un nuevo programa de robótica siguiendo la metodología aprendida en este capítulo?

---

::: practice
title: Práctica guiada · Reestructurando una aplicación de robótica

difficulty: Media

time: 60 minutos

content:

Selecciona uno de los programas desarrollados en los capítulos 8, 9 o 10 y reorganízalo siguiendo la estructura propuesta en este capítulo.

El programa deberá incluir, como mínimo:

- una sección de configuración;
- constantes claramente identificadas;
- funciones independientes para cada tarea;
- una función `main()` que coordine toda la ejecución.

Comprueba que el comportamiento del robot sigue siendo exactamente el mismo después de reorganizar el código.

:::

---

::: challenge
title: Reto · Diseña tu propia biblioteca de funciones

difficulty: Alta

content:

Crea una pequeña biblioteca de funciones reutilizables para controlar el Pioneer P3DX.

Incluye, al menos, las siguientes funciones:

- `avanzar()`
- `retroceder()`
- `girar_izquierda()`
- `girar_derecha()`
- `detener_robot()`
- `obstaculo_detectado()`

A continuación modifica los programas desarrollados anteriormente para utilizar esta biblioteca.

Analiza cuánto se simplifica el código principal y qué ventajas aporta esta organización.

:::

---

::: teacher
title: Orientaciones para el profesorado

content:

Este capítulo representa un excelente punto de transición entre la programación básica y el desarrollo de aplicaciones de robótica de mayor complejidad.

Se recomienda dedicar tiempo a revisar la calidad del código además de su funcionamiento.

El alumnado debe comprender que un programa profesional no solo debe funcionar correctamente, sino que también debe ser legible, modular y fácil de mantener.

Una actividad especialmente enriquecedora consiste en comparar diferentes soluciones desarrolladas por los estudiantes y debatir cuál presenta una mejor organización del código.

:::

---

# Resumen

Con este capítulo finalizamos la segunda parte del libro dedicada a la robótica móvil.

A lo largo de estos cinco capítulos hemos aprendido a trabajar con el Pioneer P3DX dentro de CoppeliaSim, utilizando Python para controlar sus sensores y motores, desarrollar comportamientos autónomos y estructurar aplicaciones siguiendo buenas prácticas de programación.

También hemos comprobado que la calidad de un programa no depende únicamente de que funcione correctamente.

La claridad, la reutilización del código y la facilidad de mantenimiento son aspectos fundamentales en cualquier proyecto profesional de robótica.

La estructura desarrollada en este capítulo servirá como base para todos los proyectos que construiremos a partir de ahora.

En la siguiente parte del libro ampliaremos estas capacidades incorporando nuevos sensores, técnicas de percepción más avanzadas y algoritmos que permitirán desarrollar robots cada vez más inteligentes.

---

