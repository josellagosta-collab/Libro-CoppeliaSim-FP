# Parte V. Integración de sistemas robóticos

En las partes anteriores hemos aprendido a utilizar CoppeliaSim, controlar robots móviles, desarrollar aplicaciones de visión artificial y programar robots industriales mediante Python.

Ha llegado el momento de dar un paso más.

En esta parte aprenderemos a **integrar un robot dentro de un sistema industrial completo**, donde simulación, comunicaciones, controladores, bases de datos y aplicaciones software trabajan conjuntamente para resolver problemas reales de automatización.

Comenzaremos comunicando CoppeliaSim con aplicaciones externas mediante Python y la API remota. Posteriormente descubriremos cómo integrar el simulador con **ROS 2**, utilizaremos protocolos de comunicación industrial como **OPC UA**, **MQTT** y **REST**, y construiremos un **gemelo digital** capaz de mantenerse sincronizado con una instalación física.

La parte culmina con un **proyecto industrial conectado**, en el que reuniremos todos los conocimientos adquiridos para desarrollar una célula robotizada inspirada en las utilizadas actualmente en la Industria 4.0.

::: part-cover
number: V
title: Integración de sistemas robóticos
subtitle: Comunicación, automatización e Industria 4.0 con CoppeliaSim y Python
:::

## ¿Qué aprenderás?

Al finalizar esta parte serás capaz de:

- Comunicar CoppeliaSim con aplicaciones desarrolladas en Python.
- Comprender la arquitectura cliente-servidor utilizada por la API remota.
- Integrar robots simulados con **ROS 2**.
- Utilizar protocolos industriales como **OPC UA**, **MQTT**, **TCP/IP** y **REST API**.
- Intercambiar información entre PLC, aplicaciones software y CoppeliaSim.
- Construir un gemelo digital sincronizado con una instalación física.
- Registrar información en bases de datos PostgreSQL.
- Diseñar dashboards para supervisión industrial.
- Desarrollar una arquitectura completa de Industria 4.0.
- Integrar todos los conocimientos adquiridos en un proyecto industrial conectado.

## Capítulos de esta parte

| Capítulo | Contenido |
|-----------|-----------|
| **22** | Comunicación entre CoppeliaSim y aplicaciones externas |
| **23** | Integración con ROS 2 |
| **24** | Comunicación industrial |
| **25** | Gemelo digital e Industria 4.0 |
| **26** | Proyecto industrial conectado |

## Antes de comenzar

Para aprovechar al máximo esta parte es recomendable haber completado los capítulos anteriores del libro.

En particular, se da por supuesto que el lector ya es capaz de:

- crear escenas en CoppeliaSim;
- programar aplicaciones en Python;
- controlar robots móviles e industriales;
- utilizar sensores y cámaras de visión artificial;
- desarrollar scripts para automatizar simulaciones.

Aunque muchos ejemplos continuarán ejecutándose íntegramente dentro de CoppeliaSim, el objetivo será acercarse progresivamente al funcionamiento de una instalación industrial real.

## Una visión de conjunto

En una fábrica moderna un robot nunca trabaja de forma aislada.

Habitualmente forma parte de un ecosistema formado por controladores industriales, sensores, cámaras, aplicaciones software, bases de datos y sistemas de supervisión.

Todos estos componentes intercambian información continuamente para mantener sincronizada la producción y facilitar la toma de decisiones.

Durante esta parte construiremos paso a paso una arquitectura similar a la utilizada en entornos profesionales, utilizando CoppeliaSim como plataforma de experimentación y Python como elemento integrador de todas las comunicaciones.

Al finalizar habrás desarrollado un proyecto que reproduce fielmente el funcionamiento de una célula robotizada conectada, sentando las bases para abordar los proyectos completos de la última parte del libro.

---

> *"La automatización ya no consiste únicamente en mover robots, sino en conseguir que todos los sistemas de una instalación colaboren, compartan información y trabajen como un único organismo inteligente."*