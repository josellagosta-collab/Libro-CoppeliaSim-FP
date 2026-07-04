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