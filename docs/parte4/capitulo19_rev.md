::: chapter-cover
number: 19
title: Cinemática directa e inversa
time: 6 horas
level: ★★★★☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es la cinemática de un robot industrial.
- Diferenciar la cinemática directa de la cinemática inversa.
- Entender la relación entre las articulaciones y el efector final.
- Comprender por qué la cinemática inversa simplifica enormemente la programación de un robot.
- Conocer los sistemas de referencia utilizados por el UR3.
- Comprender el papel de los objetos **Tip** y **Target** en CoppeliaSim.
- Preparar el modelo del UR3 para trabajar con cinemática inversa utilizando **CoppeliaSim EDU 4.0**.

:::

# Capítulo 19 · Cinemática directa e inversa

## Del movimiento de las articulaciones al movimiento cartesiano

En el capítulo anterior aprendimos a controlar individualmente las seis articulaciones del **Universal Robots UR3**.

Fuimos capaces de obtener los *handles* de cada eje, establecer posiciones angulares, consultar el estado de las articulaciones y ejecutar movimientos coordinados desde Python.

Ese enfoque resulta muy útil para comprender la estructura interna del robot, pero presenta una limitación importante.

Imagina que deseas recoger una pieza situada sobre una mesa.

¿Serías capaz de calcular manualmente el ángulo exacto que debe adoptar cada una de las seis articulaciones para que la herramienta llegue exactamente hasta ella?

Probablemente no.

Y, de hecho, en la industria prácticamente nadie programa un robot de esa forma.

Lo habitual consiste en indicar **la posición que debe alcanzar la herramienta**, dejando que el propio controlador del robot calcule automáticamente la configuración que deben adoptar todas las articulaciones.

Ese proceso recibe el nombre de **cinemática inversa**.

Durante este capítulo aprenderemos los fundamentos de la cinemática aplicada al UR3 y prepararemos nuestro robot para trabajar mediante coordenadas cartesianas, un método mucho más intuitivo y cercano al utilizado en las aplicaciones industriales reales.

Al finalizar el capítulo comprenderás por qué, a partir de ahora, dejaremos de pensar en ángulos articulares para empezar a pensar en posiciones dentro del espacio.

::: figure
image: ../assets/cap19/fig19_1.png
caption: Del control individual de las articulaciones al control cartesiano del efector final.
:::

::: teacher
content:

Antes de comenzar el capítulo, pide al alumnado que recuerde cómo movían el robot en el capítulo anterior.

Después plantea una pregunta sencilla:

> «Si quiero colocar la pinza exactamente sobre una pieza, ¿preferís calcular seis ángulos diferentes o indicar directamente el punto al que debe llegar?»

Este sencillo planteamiento permite introducir de forma natural el concepto de cinemática inversa.

:::

---

# 19.1 ¿Qué es la cinemática?

La **cinemática** es la rama de la robótica que estudia el movimiento de un mecanismo sin considerar las fuerzas que lo producen.

Su objetivo consiste en describir la relación existente entre las articulaciones del robot y la posición que ocupa su herramienta dentro del espacio de trabajo.

En un brazo robótico como el **UR3**, ambas cosas están íntimamente relacionadas.

Cada vez que una articulación gira, cambia automáticamente la posición del efector final.

Del mismo modo, cuando deseamos situar la herramienta en una determinada posición, será necesario calcular la configuración adecuada para todas las articulaciones.

La cinemática responde, por tanto, a dos preguntas fundamentales:

- ¿Dónde se encuentra la herramienta cuando conocemos la posición de todas las articulaciones?
- ¿Qué posición deben adoptar las articulaciones para que la herramienta alcance un punto determinado?

Estas dos cuestiones dan lugar a dos problemas diferentes, conocidos como **cinemática directa** y **cinemática inversa**.

Aunque ambos conceptos se basan en la misma relación matemática, el punto de partida en cada caso es completamente diferente.

::: figure
image: ../assets/cap19/fig19_2.png
caption: Relación existente entre las articulaciones del UR3 y la posición del efector final.
:::

---

## Un ejemplo cotidiano

Para comprender mejor este concepto, piensa en tu propio brazo.

Cuando deseas coger un vaso situado sobre una mesa no calculas conscientemente el ángulo del hombro, del codo ni de la muñeca.

Simplemente decides dónde quieres colocar la mano y tu cerebro coordina automáticamente todos los movimientos necesarios.

Un robot industrial trabaja de una forma muy similar.

La diferencia es que, en lugar de un cerebro biológico, utiliza algoritmos matemáticos capaces de calcular con gran precisión la posición que debe adoptar cada una de sus articulaciones.

Durante este capítulo utilizaremos CoppeliaSim para visualizar ese proceso sin necesidad de profundizar en formulaciones matemáticas complejas.

Nuestro objetivo será comprender **cómo trabaja el robot**, no memorizar ecuaciones.

:::: info "Objetivo del capítulo"

En este capítulo no aprenderemos a resolver matemáticamente la cinemática inversa.

Aprenderemos algo mucho más útil para nuestras prácticas: comprender cómo CoppeliaSim realiza automáticamente esos cálculos y cómo podemos aprovecharlos desde Python.

::::

---

# 19.2 Cinemática directa y cinemática inversa

En el apartado anterior vimos que la cinemática estudia la relación existente entre las articulaciones del robot y la posición del efector final.

Sin embargo, esta relación puede plantearse desde dos puntos de vista completamente diferentes.

Dependiendo de cuál sea la información conocida inicialmente hablaremos de **cinemática directa** o de **cinemática inversa**.

Ambos conceptos constituyen la base del funcionamiento de cualquier robot industrial moderno.

---

## Cinemática directa

La **cinemática directa** responde a la siguiente pregunta:

> **Si conocemos la posición de todas las articulaciones del robot, ¿dónde se encuentra el efector final?**

En este caso conocemos el ángulo de cada uno de los seis ejes del UR3.

A partir de esa información, el controlador calcula automáticamente la posición y la orientación de la herramienta.

Podemos representar este proceso mediante el siguiente esquema.

```text
Articulaciones
(Eje 1 ... Eje 6)

        │
        ▼

 Cinemática directa

        │
        ▼

Efector final

(X, Y, Z, Rx, Ry, Rz)
```

Es decir, partimos de las articulaciones y obtenemos la posición del efector final.

::: figure
image: ../assets/cap19/fig19_3.png
caption: Funcionamiento de la cinemática directa en el UR3.
:::

---

## Cinemática inversa

La **cinemática inversa** plantea exactamente el problema contrario.

En este caso la pregunta es:

> **Si queremos colocar el efector final en una posición determinada, ¿qué ángulos deben adoptar las articulaciones?**

Ahora conocemos el destino de la herramienta.

Será el propio controlador del robot quien calcule automáticamente la configuración necesaria para alcanzar ese punto.

El proceso puede representarse así.

```text
Efector final

(X, Y, Z, Rx, Ry,Rz)

        │
        ▼

 Cinemática inversa

        │
        ▼

Articulaciones

(Eje 1 ... Eje 6)
```

En robótica industrial esta es, con diferencia, la forma de trabajo más utilizada.

El programador únicamente indica el punto de destino.

El controlador calcula automáticamente la configuración de todas las articulaciones.

::: figure
image: ../assets/cap19/fig19_4.png
caption: Funcionamiento de la cinemática inversa en el UR3.
:::

---

## Comparando ambos métodos

Aunque ambos conceptos describen la misma relación entre el robot y su herramienta, parten de información diferente y persiguen objetivos distintos.

| Cinemática directa | Cinemática inversa |
|--------------------|--------------------|
| Se conocen las articulaciones. | Se conoce la posición del efector final. |
| Calcula la posición de la herramienta. | Calcula los ángulos de las articulaciones. |
| Parte del movimiento de los ejes. | Parte del objetivo que debe alcanzar la herramienta. |
| Se utiliza para conocer el estado del robot. | Se utiliza para programar movimientos industriales. |

En otras palabras:

- La **cinemática directa** responde a la pregunta **«¿Dónde está el robot?»**.
- La **cinemática inversa** responde a la pregunta **«¿Cómo debe moverse el robot para llegar a ese punto?»**.

::: teacher
content:

No es necesario profundizar todavía en los algoritmos matemáticos que resuelven la cinemática inversa.

Lo realmente importante es que el alumnado comprenda qué información conoce el robot en cada caso y cuál debe calcular automáticamente.

Más adelante comprobarán que CoppeliaSim realiza estos cálculos de forma completamente transparente.

:::

---

## ¿Cuál utilizaremos en este libro?

Aunque conoceremos ambos conceptos, durante las prácticas trabajaremos casi siempre con **cinemática inversa**.

En lugar de calcular manualmente los seis ángulos del UR3, indicaremos la posición que deseamos alcanzar y dejaremos que CoppeliaSim determine automáticamente la configuración necesaria para conseguirlo.

Este enfoque coincide con el utilizado en la mayoría de robots industriales actuales y permitirá desarrollar aplicaciones mucho más sencillas, legibles y fáciles de mantener.

Además, este método será el punto de partida para los capítulos siguientes, en los que realizaremos operaciones de manipulación, trayectorias cartesianas y tareas de **pick & place**.

---

# 19.3 Los objetos *Tip* y *Target*

Hasta ahora hemos visto que la cinemática inversa permite indicar **el punto al que queremos que llegue la herramienta**, dejando que el robot calcule automáticamente la posición de todas sus articulaciones.

Pero esto plantea una pregunta importante.

**¿Cómo sabe CoppeliaSim cuál es la posición actual del robot y cuál es el punto al que queremos que se desplace?**

La respuesta se encuentra en dos objetos auxiliares muy importantes:

- **Tip**
- **Target**

Antes de comenzar a programar movimientos cartesianos debemos comprender qué representan estos objetos y cómo prepararlos correctamente dentro de nuestra escena.

En **CoppeliaSim EDU 4.0 (rev. 0)** estos objetos **no aparecen creados automáticamente** en el modelo del UR3, por lo que tendremos que añadirlos manualmente.

---

## ¿Qué es el Tip?

El **Tip** representa la posición real del efector final.

Podemos imaginarlo como un pequeño punto situado exactamente en el extremo de la herramienta del robot.

Cada vez que las articulaciones cambian de posición, el **Tip** también cambia de posición.

Por tanto, el Tip indica en todo momento **dónde se encuentra realmente el extremo del robot**.

::: figure
image: ../assets/cap19/fig19_5.png
caption: El objeto **Tip** representa la posición real del efector final del UR3.
:::

---

## ¿Qué es el Target?

El **Target** representa el destino que deseamos alcanzar.

En lugar de mover directamente las seis articulaciones, desplazaremos este objeto por el espacio.

El solucionador de cinemática inversa intentará hacer coincidir automáticamente la posición del **Tip** con la del **Target**, calculando para ello la posición adecuada de todas las articulaciones.

Desde el punto de vista del programador, el proceso resulta mucho más sencillo.

Únicamente tendremos que indicar dónde queremos colocar el **Target**.

El resto del trabajo lo realizará CoppeliaSim.

::: figure
image: ../assets/cap19/fig19_6.png
caption: El objeto **Target** representa el punto objetivo que deberá alcanzar el efector final.
:::

---

## Trabajando juntos

Una forma muy sencilla de comprender la función de ambos objetos consiste en imaginar que paseamos a un perro utilizando una correa.

- Tú representas el **Target**.
- El perro representa el **Tip**.

Cada vez que cambias de posición, el perro intenta seguirte.

Del mismo modo, cuando desplazamos el **Target**, el robot moverá automáticamente todas sus articulaciones para que el **Tip** alcance esa nueva posición.

Esta analogía ayuda a comprender por qué ya no será necesario calcular manualmente el ángulo de cada articulación.

---

:::: info "Objetivo de este apartado"

Durante las siguientes páginas prepararemos el modelo del UR3 para trabajar
con cinemática inversa.

No escribiremos todavía ningún programa en Python.

Primero aprenderemos a crear correctamente los objetos auxiliares que
necesitaremos durante el resto del libro.

::::

---

# 19.3.1 ¿Qué es un Dummy?

Los objetos **Tip** y **Target** se crean utilizando un tipo especial de objeto denominado **Dummy**.

Un Dummy es un objeto auxiliar de CoppeliaSim.

No posee geometría, no interviene en las colisiones y tampoco representa ningún elemento físico del robot.

Su misión consiste en actuar como un **punto de referencia** dentro de la escena.

Los Dummies se utilizan en multitud de aplicaciones:

- cinemática inversa;
- trayectorias;
- sensores;
- herramientas;
- calibración;
- referencias geométricas.

En este capítulo utilizaremos dos Dummies:

- `UR3_tip`
- `UR3_target`

::: figure
image: ../assets/cap19/fig19_7.png
caption: Creación de un nuevo Dummy desde el menú Add → Dummy.
:::

---

## Creación del Tip

El primer objeto que crearemos será el **Tip**.

Para ello selecciona:

```text
Add
    └── Dummy
```

Aparecerá un nuevo Dummy dentro de la escena.

Selecciona ese objeto y cambia su nombre por:

```text
UR3_tip
```

---

## ¿Dónde debe colocarse?

El Tip debe representar el extremo real del robot.

Por ese motivo debe situarse exactamente donde termina la cadena cinemática del UR3.

En nuestro modelo esa posición corresponde al objeto:

```text
connection
```

El Dummy `UR3_tip` deberá convertirse en hijo de `connection`.

El árbol tendrá un aspecto similar al siguiente.

```text
UR3
└── ...
    └── link7_visible
        └── connection
            └── UR3_tip
```

Una vez colocado como hijo de `connection`, restablece su posición relativa para que coincida exactamente con dicho punto.

```text
X = 0
Y = 0
Z = 0
```

De esta forma el Tip acompañará automáticamente al efector final durante todos los movimientos del robot.

:::: info "¿Por qué el Tip debe ser hijo de connection?"

El objeto `connection` representa el extremo de la cadena cinemática.

Si `UR3_tip` es hijo de este objeto, cualquier movimiento de las
articulaciones hará que el Tip se desplace automáticamente junto al
efector final.

De este modo siempre conoceremos la posición real de la herramienta.

::::

---

# 19.3.2 Creación del Target

El segundo objeto que necesitaremos será el **Target**.

Al igual que el Tip, también se crea mediante un Dummy.

Selecciona nuevamente:

```text
Add
    └── Dummy
```

Renombra el nuevo objeto como:

```text
UR3_target
```

Hasta este punto ambos objetos son idénticos.

La diferencia aparece al colocarlos dentro del árbol de la escena.

---

## ¿Dónde debe colocarse el Target?

En versiones recientes de CoppeliaSim es habitual dejar el Target completamente independiente del robot.

Sin embargo, **en CoppeliaSim EDU 4.0 (rev. 0)** el asistente **Inverse Kinematics Generator** únicamente busca los objetos pertenecientes al modelo seleccionado.

Por este motivo el objeto `UR3_target` deberá colocarse como **hijo directo del modelo UR3**.

Su posición dentro del árbol será similar a la siguiente.

```text
UR3
├── Script
├── UR3_target
└── joint
    └── ...
        └── connection
            └── UR3_tip
```

Es importante observar que:

- `UR3_tip` es hijo de `connection`.
- `UR3_target` es hijo directo de `UR3`.

No debe situarse dentro de la cadena cinemática del robot.

::: figure
image: ../assets/cap19/fig19_8.png
caption: Organización correcta del árbol del UR3 con los objetos UR3_tip y UR3_target.
:::

:::: common-error "Un error muy frecuente"

No conviertas `UR3_target` en hijo de `connection` ni de ninguna de las
articulaciones del robot.

Si lo haces, el Target se moverá junto con el propio robot y la
cinemática inversa dejará de tener sentido.

En la versión EDU 4.0 el Target debe ser **hijo del modelo UR3**, pero
nunca de la cadena cinemática.

::::

---

## Comprobación de la escena

Antes de continuar verifica que el árbol tiene un aspecto similar al siguiente.

```text
UR3
├── Script
├── UR3_target
└── joint
    └── ...
        └── connection
            └── UR3_tip
```

Si la estructura coincide con la mostrada, la escena ya está preparada para generar automáticamente el grupo de cinemática inversa.

En el siguiente apartado utilizaremos el asistente **Inverse Kinematics Generator** para crear toda la configuración necesaria sin tener que programarla manualmente.

---

# 19.3.3 Generación automática de la cinemática inversa

Una vez creados los objetos **UR3_tip** y **UR3_target**, ya podemos preparar el robot para trabajar con cinemática inversa.

En **CoppeliaSim EDU 4.0 (rev. 0)** este proceso se realiza mediante un asistente denominado **Inverse Kinematics Generator**.

Este asistente analiza automáticamente la cadena cinemática comprendida entre la base del robot y el objeto **Tip**, creando toda la configuración necesaria para resolver la cinemática inversa.

No será necesario crear manualmente grupos IK ni configurar cada articulación individualmente.

---

## Abrir el generador

Selecciona en la barra de menús:

```text
Modules
└── Kinematics
      └── Inverse Kinematics Generator...
```

Aparecerá la ventana de configuración del asistente.

::: figure
image: ../assets/cap19/fig19_9.png
caption: Ventana del asistente **Inverse Kinematics Generator** de CoppeliaSim EDU 4.0.
:::

---

## Configuración del asistente

Completa los diferentes campos utilizando los objetos que hemos preparado anteriormente.

| Campo | Valor recomendado |
|--------|-------------------|
| Robot model | UR3 |
| Robot base | UR3 |
| Robot tip | UR3_tip |
| Robot target | UR3_target |
| Joint group | *(dejar vacío)* |

El resto de parámetros puede mantenerse con los valores predeterminados.

En particular:

- Posición → X, Y y Z activados.
- Orientación → Alpha+Beta y Gamma activados.
- Handling → Enabled, During simulation y When not simulating activados.

---

## ¿Por qué dejamos vacío el campo Joint group?

Puede llamar la atención que este campo permanezca vacío.

Sin embargo, el propio asistente indica:

```text
leave empty to use all joints in the tip-target chain
```

Esto significa que el generador localizará automáticamente todas las articulaciones comprendidas entre el objeto **UR3_tip** y la base del robot.

En el caso del UR3 esto incluye las seis articulaciones del manipulador.

Por tanto, no es necesario crear previamente ningún grupo de articulaciones.

::: common-error
content:

Un error frecuente consiste en intentar crear un **Joint group** antes de utilizar el asistente.

En el modelo del UR3 utilizado en este libro no es necesario.

Basta con dejar este campo vacío para que el generador detecte automáticamente toda la cadena cinemática.

:::

---

## Generar la configuración IK

Una vez revisados todos los parámetros, pulsa el botón **Generate**.

El asistente analizará el modelo y creará automáticamente la configuración necesaria para resolver la cinemática inversa.

A diferencia de versiones más recientes de CoppeliaSim, esta configuración no aparece integrada dentro del árbol del robot.

En su lugar se crea un nuevo objeto denominado **IK**, situado al mismo nivel que el modelo del UR3.

::: figure
image: ../assets/cap19/fig19_10.png
caption: Árbol de la escena tras generar automáticamente la configuración de cinemática inversa.
:::

---

## Comprobando el resultado

Después de ejecutar el generador, el árbol de la escena deberá presentar un aspecto similar al siguiente.

```text
new scene
│
├── Floor
├── UR3
│   ├── Script
│   ├── UR3_target
│   └── ...
│       └── connection
│           └── UR3_tip
│
└── IK
```

Observa dos aspectos importantes.

- Los objetos **UR3_tip** y **UR3_target** permanecen exactamente donde los habíamos colocado.
- El asistente añade un nuevo objeto denominado **IK**, encargado de gestionar la cinemática inversa del robot.

No es necesario modificar este nuevo objeto.

Durante las prácticas trabajaremos directamente con **UR3_target**.

---

## La escena ya está preparada

Llegados a este punto ya disponemos de todos los elementos necesarios para comenzar a trabajar mediante coordenadas cartesianas.

A partir de ahora dejaremos de indicar los ángulos de las articulaciones y comenzaremos a mover el robot desplazando únicamente el objeto **UR3_target**.

En los siguientes apartados aprenderemos a expresar esas posiciones utilizando coordenadas cartesianas y posteriormente accederemos a ellas desde Python.

---

# 19.4 Coordenadas cartesianas y sistemas de referencia

Una vez preparada la escena para trabajar con cinemática inversa, ya estamos en condiciones de indicar al robot **dónde queremos que se desplace**.

Pero surge una nueva pregunta.

**¿Cómo describimos una posición dentro del espacio?**

La respuesta es mediante un **sistema de coordenadas cartesianas**.

Este sistema permite definir con precisión cualquier punto del espacio utilizando únicamente tres valores numéricos.

A partir de este momento dejaremos de pensar en ángulos articulares y comenzaremos a trabajar mediante posiciones cartesianas.

---

## El sistema de coordenadas XYZ

CoppeliaSim utiliza un sistema de coordenadas tridimensional formado por tres ejes perpendiculares entre sí.

- **Eje X** → desplazamiento izquierda – derecha.
- **Eje Y** → desplazamiento delante – detrás.
- **Eje Z** → desplazamiento vertical.

Cada punto del espacio queda definido mediante tres coordenadas.

```text
X = 0.35
Y = -0.15
Z = 0.25
```

En este ejemplo estamos indicando una posición situada:

- 35 cm sobre el eje X.
- 15 cm en sentido negativo del eje Y.
- 25 cm de altura respecto al origen.

::: figure
image: ../assets/cap19/fig19_11.png
caption: Sistema de coordenadas cartesianas utilizado por CoppeliaSim.
:::

---

## Importante: CoppeliaSim trabaja en metros

Este aspecto suele sorprender a quienes comienzan a trabajar con CoppeliaSim.

Aunque muchos robots industriales se programan utilizando milímetros, **CoppeliaSim utiliza metros como unidad de longitud**.

Por ejemplo:

| Metros | Milímetros |
|---------|------------:|
| 0.10 | 100 mm |
| 0.25 | 250 mm |
| 0.35 | 350 mm |
| 0.50 | 500 mm |

Siempre que utilicemos funciones como:

```python
sim.setObjectPosition()

sim.getObjectPosition()
```

las coordenadas estarán expresadas en **metros**.

::: common-error
content:

Uno de los errores más frecuentes consiste en introducir directamente valores en milímetros.

Por ejemplo:

```python
[350, -150, 250]
```

Esto desplazará el objeto cientos de metros fuera de la escena.

Lo correcto será:

```python
[0.35, -0.15, 0.25]
```

:::

---

## El origen de coordenadas

Todo sistema cartesiano necesita un punto de referencia denominado **origen**.

En la escena del UR3 este origen coincide inicialmente con el sistema de referencia global de la escena.

Todas las posiciones que utilizaremos durante este capítulo estarán referidas a ese sistema global.

Más adelante aprenderemos a utilizar referencias locales para expresar posiciones relativas a otros objetos.

::: figure
image: ../assets/cap19/fig19_12.png
caption: Origen del sistema de coordenadas global utilizado durante las primeras prácticas.
:::

---

# Posición y orientación

Hasta ahora únicamente hemos indicado posiciones.

Sin embargo, una herramienta no solo debe llegar a un punto determinado.

También debe hacerlo con la orientación adecuada.

Imagina una pinza que debe recoger una pieza.

Aunque llegue exactamente al punto correcto, la operación fracasará si la herramienta está girada de forma incorrecta.

Por este motivo, la posición completa de un efector final queda definida mediante seis parámetros.

| Parámetro | Significado |
|-----------|-------------|
| X | Posición respecto al eje X |
| Y | Posición respecto al eje Y |
| Z | Posición respecto al eje Z |
| Rx | Giro alrededor del eje X |
| Ry | Giro alrededor del eje Y |
| Rz | Giro alrededor del eje Z |

Los tres primeros representan la **posición**.

Los tres últimos representan la **orientación**.

::: figure
image: ../assets/cap19/fig19_13.png
caption: Posición y orientación del efector final mediante seis grados de libertad.
:::

---

## ¿Por qué todavía no modificaremos la orientación?

Aunque el robot puede controlar simultáneamente posición y orientación, durante las primeras prácticas trabajaremos únicamente con cambios de posición.

Mantendremos constante la orientación del efector final.

Este enfoque permitirá comprender mucho mejor el funcionamiento de la cinemática inversa antes de comenzar a trabajar con movimientos más complejos.

Más adelante aprenderemos a modificar también la orientación del **Target**, consiguiendo que el robot cambie la inclinación de su herramienta.

---

## Visualizando los ejes en CoppeliaSim

Selecciona el objeto **UR3_target** dentro del árbol de la escena.

Observarás que aparece un pequeño sistema de ejes de colores.

Cada color identifica uno de los ejes cartesianos.

- Rojo → eje X.
- Verde → eje Y.
- Azul → eje Z.

Estos ejes permiten conocer de un vistazo la orientación del objeto y facilitan enormemente la programación de movimientos cartesianos.

Durante las próximas prácticas utilizaremos continuamente estos indicadores para comprobar el sentido de los desplazamientos.

::: figure
image: ../assets/cap19/fig19_14.png
caption: Ejes cartesianos mostrados al seleccionar el objeto UR3_target.
:::

---

## Preparando la programación desde Python

Ya disponemos de todos los elementos necesarios para comenzar a programar movimientos mediante coordenadas cartesianas.

Nuestra escena contiene:

- el modelo del UR3;
- el objeto **UR3_tip**;
- el objeto **UR3_target**;
- la configuración automática de cinemática inversa generada por CoppeliaSim.

En el siguiente apartado aprenderemos a acceder al objeto **UR3_target** desde Python y a modificar su posición utilizando la API remota.

Será el primer programa en el que moveremos el robot indicando únicamente el punto que debe alcanzar el efector final.

---

# 19.5 Moviendo el *Target* desde Python

Hasta este momento hemos preparado completamente la escena.

Disponemos de:

- el modelo del **UR3**;
- el objeto **UR3_tip**, situado en el extremo del robot;
- el objeto **UR3_target**, que utilizaremos como objetivo;
- la configuración de cinemática inversa generada automáticamente mediante el asistente **Inverse Kinematics Generator**.

Ha llegado el momento de comenzar a controlar el robot desde Python.

A diferencia del capítulo anterior, ya no modificaremos directamente el ángulo de cada articulación.

Nuestro programa únicamente moverá el objeto **UR3_target**.

Será CoppeliaSim quien calcule automáticamente la posición que deben adoptar las seis articulaciones del robot.

---

## Accediendo al Target

Como cualquier otro objeto de CoppeliaSim, el Target posee un identificador (*handle*) que nos permitirá acceder a él desde Python.

Podemos obtenerlo utilizando la función `sim.getObject()`.

```python
target = sim.getObject('/UR3/UR3_target')
```

Observa que la ruta comienza por:

```text
/UR3/
```

Esto se debe a que, en **CoppeliaSim EDU 4.0**, el objeto **UR3_target** forma parte del modelo del robot y aparece como hijo directo de `UR3`.

Una vez obtenido el *handle*, podremos consultar y modificar su posición.

::: figure
image: ../assets/cap19/fig19_15.png
caption: Obtención del identificador del objeto **UR3_target** mediante `sim.getObject()`.
:::

---

## Comprobando el identificador obtenido

Antes de comenzar a mover el robot resulta recomendable comprobar que el objeto se ha localizado correctamente.

Podemos hacerlo mostrando su identificador por pantalla.

```python
target = sim.getObject('/UR3/UR3_target')

print(target)
```

Si todo ha ido correctamente, Python mostrará un número entero distinto de cero.

Ese número representa el identificador interno asignado por CoppeliaSim al objeto.

Si aparece un mensaje de error, revisa que el nombre del objeto coincida exactamente con el del árbol de la escena.

::: common-error
content:

La función `sim.getObject()` distingue entre mayúsculas y minúsculas.

Los siguientes nombres son diferentes:

- `UR3_target`
- `ur3_target`
- `Target`

Comprueba siempre el nombre directamente en el árbol de la escena.

:::

---

## Leyendo la posición del Target

La función `sim.getObjectPosition()` devuelve la posición de un objeto respecto a un sistema de referencia.

Su utilización es muy sencilla.

```python
posicion = sim.getObjectPosition(target, -1)

print(posicion)
```

Obtendremos una lista con tres valores.

```text
[X, Y, Z]
```

Por ejemplo:

```text
[0.35, -0.15, 0.25]
```

Estos valores representan la posición actual del Target expresada en metros.

::: figure
image: ../assets/cap19/fig19_16.png
caption: Lectura de la posición cartesiana del objeto **UR3_target**.
:::

---

## ¿Qué significa el valor -1?

En la llamada anterior aparece un parámetro que merece una breve explicación.

```python
sim.getObjectPosition(target, -1)
```

El segundo argumento indica respecto a qué sistema de referencia queremos obtener la posición.

Cuando utilizamos:

```python
-1
```

estamos indicando que deseamos expresar la posición respecto al sistema de coordenadas global de la escena.

Durante este capítulo trabajaremos siempre utilizando esta referencia.

Más adelante aprenderemos a utilizar otros sistemas de referencia, como el propio robot o diferentes objetos de la escena.

---

## Modificando la posición del Target

Para desplazar el objeto utilizaremos la función `sim.setObjectPosition()`.

```python
sim.setObjectPosition(
    target,
    -1,
    [0.35, -0.15, 0.25]
)
```

En este ejemplo estamos indicando que el Target deberá situarse en:

- X = 0.35 m
- Y = -0.15 m
- Z = 0.25 m

Una vez ejecutada esta instrucción, el solucionador de cinemática inversa calculará automáticamente la posición necesaria para que el efector final alcance ese punto.

::: figure
image: ../assets/cap19/fig19_17.png
caption: Desplazamiento del objeto **UR3_target** mediante `sim.setObjectPosition()`.
:::

---

## ¿Qué ocurre internamente?

Aunque nuestro programa únicamente modifica la posición del Target, internamente CoppeliaSim realiza un proceso mucho más complejo.

De forma simplificada, los pasos son los siguientes:

1. Python modifica la posición del objeto **UR3_target**.
2. El sistema de cinemática inversa calcula una nueva solución.
3. Se determina la posición adecuada para cada una de las seis articulaciones.
4. El robot comienza a moverse.
5. El objeto **UR3_tip** alcanza finalmente la posición del Target.

Todo este proceso ocurre automáticamente.

Desde el punto de vista del programador, únicamente estamos cambiando tres números.

::: figure
image: ../assets/cap19/fig19_18.png
caption: Funcionamiento interno de la cinemática inversa tras modificar el Target.
:::

---

## Ventajas de este método

Comparado con el control directo de las articulaciones, este sistema presenta numerosas ventajas.

- El código es mucho más sencillo.
- No es necesario calcular ángulos.
- Los programas son más fáciles de comprender.
- Las trayectorias resultan más naturales.
- Se aproxima a la forma de programación utilizada en robots industriales reales.

Por este motivo, todos los ejemplos desarrollados a partir de este capítulo utilizarán este método de trabajo.

---

## Una primera prueba

Antes de continuar, realiza una sencilla comprobación.

1. Ejecuta la simulación.
2. Lanza el programa anterior.
3. Observa el movimiento del UR3.
4. Comprueba que el efector final intenta alcanzar la posición indicada.

Si todo funciona correctamente, significa que:

- el objeto **UR3_target** está correctamente localizado;
- la configuración IK se ha generado correctamente;
- el robot está preparado para realizar movimientos cartesianos desde Python.

Este será el punto de partida para todas las prácticas de manipulación que desarrollaremos en los siguientes capítulos.

---

# 19.6 Verificando el funcionamiento de la cinemática inversa

Después de crear los objetos **UR3_tip** y **UR3_target**, generar automáticamente la configuración de cinemática inversa y acceder al Target desde Python, conviene realizar una última comprobación antes de continuar con los siguientes capítulos.

El objetivo consiste en verificar que todos los elementos de la escena funcionan correctamente y que el robot responde como esperamos.

Esta pequeña comprobación servirá además para detectar posibles errores de configuración antes de comenzar a desarrollar aplicaciones más complejas.

---

## Comprobación manual

Antes de ejecutar ningún programa en Python, realiza las siguientes comprobaciones.

1. Comprueba que el árbol de la escena contiene los objetos:

   - `UR3`
   - `UR3_tip`
   - `UR3_target`
   - `IK`

2. Verifica que:

   - `UR3_tip` es hijo de `connection`.
   - `UR3_target` es hijo directo de `UR3`.

3. Inicia la simulación.

4. Selecciona el objeto **UR3_target**.

5. Utiliza el manipulador de traslación para desplazar ligeramente el Target.

Si la configuración es correcta, observarás que el UR3 mueve automáticamente todas sus articulaciones intentando que el objeto **UR3_tip** alcance la nueva posición.

::: figure
image: ../assets/cap19/fig19_19.png
caption: Comprobación manual del funcionamiento de la cinemática inversa desplazando el objeto **UR3_target**.
:::

---

## Comprobación desde Python

Una vez comprobado el funcionamiento manual, podemos realizar la misma operación desde Python.

El siguiente ejemplo obtiene el identificador del Target, consulta su posición y posteriormente modifica ligeramente la coordenada X.

```python
target = sim.getObject('/UR3/UR3_target')

posicion = sim.getObjectPosition(target, -1)

print("Posición inicial:", posicion)

nueva_posicion = [
    posicion[0] + 0.05,
    posicion[1],
    posicion[2]
]

sim.setObjectPosition(target, -1, nueva_posicion)
```

Al ejecutar este programa, el Target avanzará cinco centímetros sobre el eje X.

El solucionador de cinemática inversa calculará automáticamente la nueva posición de todas las articulaciones del UR3.

---

## ¿Qué debemos observar?

Durante la ejecución presta atención a los siguientes aspectos.

- El movimiento debe ser continuo.
- El robot debe desplazarse sin saltos bruscos.
- El objeto **UR3_tip** debe aproximarse al **UR3_target**.
- Ninguna articulación debe moverse de forma independiente; todas colaboran para alcanzar el objetivo.

Si todo ocurre de esta manera, la escena está correctamente preparada para desarrollar aplicaciones de manipulación.

::: common-error
content:

Si el robot no se mueve al desplazar el **UR3_target**, revisa los siguientes puntos:

- El objeto `UR3_tip` debe ser hijo de `connection`.
- El objeto `UR3_target` debe ser hijo directo de `UR3`.
- Debe existir el objeto `IK` generado por el asistente.
- El nombre del Target debe coincidir exactamente con el utilizado en el programa Python.
- La simulación debe estar en ejecución.

:::

---

## Preparados para el siguiente capítulo

En este capítulo hemos aprendido cómo preparar un robot para trabajar mediante cinemática inversa.

A partir de ahora dejaremos de pensar en ángulos articulares y comenzaremos a programar movimientos indicando únicamente el punto que debe alcanzar la herramienta.

En el siguiente capítulo aprenderemos a aprovechar esta capacidad para desarrollar las primeras operaciones de manipulación industrial.

Comenzaremos creando secuencias de aproximación, recogida y depósito de objetos, construyendo nuestras primeras aplicaciones de **Pick & Place**.

---

# 19.7 Práctica guiada

::: practice
title: Preparación del UR3 para trabajar con cinemática inversa

difficulty: Media

time: 60 minutos

content:

Realiza las siguientes actividades.

1. Abre la escena del UR3 utilizada durante este capítulo.

2. Crea el objeto `UR3_tip`.

3. Sitúalo como hijo de `connection`.

4. Crea el objeto `UR3_target`.

5. Colócalo como hijo directo del modelo `UR3`.

6. Ejecuta el asistente **Inverse Kinematics Generator**.

7. Comprueba que aparece el objeto `IK`.

8. Ejecuta la simulación.

9. Desplaza manualmente el objeto `UR3_target`.

10. Comprueba que el robot adapta automáticamente la posición de todas sus articulaciones.

11. Obtén el *handle* del Target desde Python.

12. Lee su posición mediante `sim.getObjectPosition()`.

13. Modifica la coordenada X utilizando `sim.setObjectPosition()`.

14. Observa cómo responde el robot.

Al finalizar la práctica deberás ser capaz de preparar completamente un modelo del UR3 para trabajar con cinemática inversa.

:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Cinemática | Relación entre las articulaciones y la posición del efector final. |
| Cinemática directa | Obtiene la posición del efector final a partir de las articulaciones. |
| Cinemática inversa | Calcula las articulaciones necesarias para alcanzar una posición. |
| Dummy | Objeto auxiliar utilizado como punto de referencia. |
| Tip | Punto que representa la posición real del efector final. |
| Target | Punto objetivo que debe alcanzar el efector final. |
| IK | Configuración encargada de resolver la cinemática inversa. |
| Coordenadas cartesianas | Sistema XYZ utilizado para definir posiciones. |
| Sistema global | Sistema de referencia respecto al que se expresan inicialmente las posiciones. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender la diferencia entre cinemática directa y cinemática inversa.
- ✅ Crear manualmente los objetos `UR3_tip` y `UR3_target`.
- ✅ Preparar correctamente el árbol del modelo del UR3.
- ✅ Generar automáticamente la configuración IK mediante el asistente de CoppeliaSim.
- ✅ Leer la posición cartesiana del Target desde Python.
- ✅ Modificar la posición del Target mediante programación.
- ✅ Comprobar el correcto funcionamiento de la cinemática inversa.

Con esta base ya estás preparado para comenzar a desarrollar aplicaciones de manipulación industrial.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre la cinemática directa y la cinemática inversa?

2. ¿Qué función desempeña el objeto **UR3_tip**?

3. ¿Qué representa el objeto **UR3_target**?

4. ¿Por qué el objeto `UR3_target` debe ser hijo del modelo `UR3` en CoppeliaSim EDU 4.0?

5. ¿Qué función realiza el objeto `IK` generado automáticamente?

6. ¿Por qué el campo **Joint group** debe dejarse vacío al utilizar el asistente?

7. ¿Qué unidades utiliza CoppeliaSim para expresar posiciones?

8. ¿Qué función permite modificar la posición del Target desde Python?

---

## Reto

::: challenge
title: Explorando el espacio de trabajo del UR3

content:

Realiza varias pruebas modificando únicamente una coordenada cada vez.

- Cambia únicamente la coordenada **X**.
- Repite el experimento modificando únicamente **Y**.
- Finalmente modifica únicamente **Z**.

Después responde a las siguientes preguntas.

- ¿Qué articulaciones intervienen principalmente en cada movimiento?
- ¿Existe alguna dirección en la que el robot tenga mayores dificultades para desplazarse?
- ¿Qué ocurre cuando intentas alcanzar una posición situada fuera del espacio de trabajo del robot?

Anota tus conclusiones y compáralas con las de tus compañeros.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Comprender la cinemática inversa.
- Preparar correctamente el modelo del UR3.
- Familiarizar al alumnado con los objetos Tip, Target e IK.
- Introducir el control cartesiano desde Python.

**Material necesario**

- CoppeliaSim EDU 4.0 correctamente instalado.
- Python configurado con la API remota.
- Escena del UR3 utilizada durante esta parte del libro.

**Sugerencias metodológicas**

Antes de comenzar la programación, dedica unos minutos a que el alumnado manipule manualmente el objeto **UR3_target**.

Observar cómo el robot adapta automáticamente todas sus articulaciones ayuda enormemente a comprender el funcionamiento de la cinemática inversa y facilita la transición hacia la programación mediante coordenadas cartesianas.

:::

---

## Próximo capítulo

Ya somos capaces de controlar el efector final indicando únicamente la posición que debe alcanzar.

En el siguiente capítulo aprenderemos a aprovechar esta capacidad para construir las primeras secuencias de manipulación industrial.

El UR3 se aproximará a una pieza, la recogerá, la transportará y la depositará en otra posición, desarrollando nuestras primeras aplicaciones completas de **Pick & Place**.


