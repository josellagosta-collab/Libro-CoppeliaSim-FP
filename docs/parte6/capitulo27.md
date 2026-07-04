# Capítulo 27. Manipulación robótica con brazos industriales

## Objetivos del capítulo

Al finalizar este capítulo el alumno será capaz de:

- Comprender qué es un manipulador robótico industrial.
- Identificar los diferentes elementos que forman un brazo robot.
- Diferenciar entre articulaciones y grados de libertad.
- Manipular un brazo robótico dentro de CoppeliaSim.
- Controlar sus articulaciones desde la interfaz del simulador.
- Preparar el entorno para su posterior programación mediante Python.

---

# 27.1 Introducción

Hasta este momento del libro hemos trabajado principalmente con robots móviles, sensores, visión artificial y comunicaciones entre Python y CoppeliaSim. En esta última parte nos centraremos en uno de los campos más importantes de la automatización industrial: la **manipulación robótica**.

Un brazo robot es una máquina diseñada para mover objetos de forma precisa dentro de un espacio de trabajo. Gracias a sus múltiples articulaciones puede posicionar herramientas o piezas con gran exactitud, lo que lo convierte en un elemento imprescindible en líneas de producción, laboratorios, centros logísticos y aplicaciones de investigación.

Actualmente encontramos brazos robóticos realizando tareas como:

- montaje de componentes electrónicos;
- soldadura;
- pintura industrial;
- manipulación de materiales;
- clasificación automática;
- paletizado;
- inspección mediante visión artificial;
- operaciones colaborativas junto a personas.

CoppeliaSim incorpora numerosos modelos de robots industriales que permiten experimentar con este tipo de sistemas sin necesidad de disponer del costoso hardware físico.

En este capítulo aprenderemos a manejar estos robots desde el simulador antes de comenzar su programación mediante Python en los capítulos siguientes.

![Figura 27.1. Brazos robóticos industriales utilizados en distintos sectores](../imagenes/cap27/fig27_01.png)

**Figura 27.1.** Ejemplos de brazos robóticos empleados en aplicaciones industriales.

---

# 27.2 ¿Qué es un manipulador robótico?

Un manipulador robótico es un mecanismo formado por una cadena de eslabones unidos mediante articulaciones móviles. El movimiento coordinado de todas ellas permite desplazar una herramienta situada en el extremo del robot hasta una posición determinada.

En robótica industrial suele utilizarse la siguiente terminología:

- **Base:** estructura fija sobre la que se apoya el robot.
- **Articulación (Joint):** elemento que permite el movimiento entre dos eslabones.
- **Eslabón (Link):** parte rígida situada entre dos articulaciones.
- **Muñeca (Wrist):** conjunto de las últimas articulaciones responsables de orientar la herramienta.
- **Efector final (End Effector):** herramienta que realiza el trabajo, por ejemplo una pinza, una ventosa o un soldador.

Cada fabricante desarrolla diferentes configuraciones mecánicas dependiendo de la aplicación, aunque todas ellas comparten estos mismos elementos fundamentales.

![Figura 27.2. Partes principales de un brazo robótico industrial](../imagenes/cap27/fig27_02.png)

**Figura 27.2.** Componentes fundamentales de un manipulador robótico.

Los brazos robóticos modernos incorporan además sensores internos capaces de medir continuamente la posición de cada articulación. Gracias a esta información el controlador puede calcular con precisión la postura completa del robot y corregir cualquier desviación durante el movimiento.

En los siguientes apartados comenzaremos a trabajar directamente con uno de estos robots dentro de CoppeliaSim para comprender su funcionamiento desde un punto de vista práctico.