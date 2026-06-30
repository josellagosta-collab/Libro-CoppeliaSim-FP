# Capítulo 2. Instalación y configuración inicial de CoppeliaSim

!!! abstract "Objetivos del capítulo"

    Al finalizar este capítulo serás capaz de:

    - Descargar correctamente CoppeliaSim EDU.
    - Comprender la diferencia entre las distintas versiones disponibles.
    - Instalar CoppeliaSim en Windows.
    - Conocer la estructura de carpetas del programa.
    - Configurar el entorno de trabajo para el resto del libro.
    - Realizar la primera ejecución del simulador.

---

# 2.1 Introducción

Antes de comenzar a programar robots necesitamos preparar correctamente nuestro entorno de trabajo.

Una instalación incorrecta puede provocar problemas más adelante cuando intentemos conectar Python con CoppeliaSim o cuando carguemos determinadas escenas.

Por este motivo dedicaremos un capítulo completo a instalar y comprender el programa antes de escribir una sola línea de código.

!!! tip "Consejo para el profesor"

    Aunque algunos alumnos ya tengan instalado CoppeliaSim, es recomendable realizar la instalación completa con todo el grupo. Así todos partirán del mismo entorno y será mucho más sencillo resolver incidencias.

---

# 2.2 Versiones de CoppeliaSim

Actualmente Coppelia Robotics distribuye varias ediciones del simulador.

| Versión | Destinatarios | Uso recomendado |
|----------|---------------|-----------------|
| EDU | Educación | ✔ Este libro |
| Pro | Empresas | Automatización industrial |
| Headless | Servidores | Ejecución sin interfaz gráfica |

Durante todo el libro utilizaremos:

**CoppeliaSim EDU 4.10.0 (rev.0)**

que es completamente suficiente para todos los ejercicios propuestos.

---

# 2.3 Descarga

La descarga debe realizarse siempre desde la página oficial.

!!! warning "Importante"

    No descargues CoppeliaSim desde páginas de terceros.

    Utiliza siempre la versión publicada por **Coppelia Robotics**.

Una vez descargado el instalador tendremos un archivo similar a:

```text
CoppeliaSim_Edu_4_10_0_rev0_Windows.exe
```

---

# 2.4 Instalación

La instalación es muy sencilla.

1. Ejecutar el instalador.
2. Aceptar la licencia.
3. Seleccionar la carpeta de instalación.
4. Esperar a que finalice la copia de archivos.

En este libro asumiremos la siguiente ubicación:

```text
C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu
```

Si has elegido otra carpeta no ocurre nada.

Simplemente deberás recordar su ubicación.

---

# 2.5 Primer inicio

Al ejecutar CoppeliaSim por primera vez aparecerá una ventana similar a esta.

*(En la versión definitiva del libro se incluirá una captura de pantalla de la interfaz con llamadas numeradas.)*

Durante el primer inicio es posible que aparezcan mensajes relacionados con:

- licencia
- OpenGL
- configuración gráfica

En la mayoría de los casos basta con aceptar la configuración por defecto.

---

# 2.6 La estructura de carpetas

Una de las ventajas de CoppeliaSim es que prácticamente todos sus recursos se encuentran organizados en carpetas.

La estructura puede variar ligeramente entre versiones, pero normalmente encontraremos algo parecido a lo siguiente.

```text
CoppeliaSimEdu/

├── scenes/
├── models/
├── programs/
├── addOns/
├── lua/
├── python/
├── textures/
├── fonts/
├── system/
└── helpFiles/
```

Veamos qué contiene cada una de ellas.

---

## scenes

Aquí se encuentran las escenas de ejemplo.

Son probablemente la carpeta que más utilizaremos durante este libro.

Encontraremos ejemplos de:

- robots móviles
- brazos robóticos
- fábricas
- sensores
- cámaras
- drones

---

## models

Contiene modelos reutilizables.

Por ejemplo:

- robots
- mesas
- edificios
- cintas transportadoras
- cámaras
- personas

Estos modelos aparecen también en el **Model Browser**.

---

## addOns

Contiene complementos que amplían las capacidades del simulador.

Durante este libro no modificaremos esta carpeta.

---

## textures

Almacena las texturas utilizadas por los objetos 3D.

---

## python

En versiones recientes incluye ejemplos relacionados con Python y herramientas auxiliares.

---

## system

Contiene archivos internos necesarios para el funcionamiento del simulador.

!!! warning "No modificar"

    Nunca elimines ni modifiques archivos de esta carpeta salvo que la documentación oficial lo indique expresamente.

---

# 2.7 Configuración recomendada

Antes de continuar conviene realizar una pequeña configuración.

## Activar el árbol de objetos

Comprueba que el panel **Scene Hierarchy** está visible.

Si no aparece:

```text
View → Scene hierarchy
```

---

## Activar el navegador de modelos

Comprueba que el panel **Model Browser** está visible.

En caso contrario:

```text
View → Model browser
```

---

## Restaurar la distribución de ventanas

Si alguna ventana ha desaparecido accidentalmente es posible restaurar la disposición inicial desde:

```text
View → Default layout
```

---

# 2.8 La primera escena

Nada más abrir CoppeliaSim aparecerá una escena vacía.

Normalmente contiene:

- una cámara
- un suelo
- una luz

Esta será nuestra plantilla inicial.

Más adelante aprenderemos a abrir escenas mucho más complejas.

---

# 2.9 Guardar una escena

Una escena contiene todos los objetos necesarios para una simulación.

Para guardarla:

```text
File → Save scene as...
```

La extensión utilizada por CoppeliaSim es:

```text
.ttt
```

Ejemplo:

```text
practica01.ttt
```

---

# 2.10 Buenas prácticas

A medida que avancemos en el libro iremos creando numerosas escenas.

Es recomendable utilizar una estructura como la siguiente:

```text
Robotica/

├── Practica01/
│      practica01.ttt
│
├── Practica02/
│      practica02.ttt
│
├── Practica03/
│      practica03.ttt
│
└── Recursos/
```

Esto facilitará enormemente la organización del trabajo.

---

# Resumen

En este capítulo hemos instalado correctamente CoppeliaSim y hemos conocido la organización básica de sus carpetas.

También hemos preparado el entorno para comenzar a trabajar de forma cómoda durante el resto del libro.

En el siguiente capítulo estudiaremos con detalle la interfaz del simulador y aprenderemos el significado de cada uno de sus paneles, botones e iconos.

---

# Actividades

1. Localiza la carpeta `scenes`.

2. Localiza la carpeta `models`.

3. Crea una carpeta llamada `Robotica`.

4. Dentro de ella crea la carpeta `Practica01`.

5. Guarda una escena vacía con el nombre:

```text
practica01.ttt
```

---

# Autoevaluación

1. ¿Qué extensión utilizan las escenas de CoppeliaSim?

2. ¿Qué carpeta contiene los modelos reutilizables?

3. ¿Qué carpeta contiene las escenas de ejemplo?

4. ¿Qué panel muestra todos los objetos de la escena?

5. ¿Por qué es importante mantener organizada la estructura de carpetas?