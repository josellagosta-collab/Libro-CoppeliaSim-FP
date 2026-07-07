# Escena para Pick and Place con UR3 y RG2

Esta escena permite ejecutar el script:

```powershell
.\.venv\Scripts\python.exe copellia_practicas\cap20_manipulacion\pick_and_place_ur3_rg2.py
```

Archivo de escena recomendado:

```text
copellia_practicas/cap20_manipulacion/cap20_pick_and_place_ur3_rg2.ttt
```

Si abres esa escena y quieres crear automaticamente la pieza y la zona de deposito, ejecuta:

```powershell
.\.venv\Scripts\python.exe copellia_practicas\cap20_manipulacion\preparar_escena_pick_and_place.py
```

El objetivo es que el UR3 recoja una pieza situada a la derecha/frente del robot y la deposite en una segunda posicion segura.

## Elementos necesarios

| Elemento | Nombre en CoppeliaSim | Funcion |
|---|---|---|
| Robot industrial | `UR3` | Manipulador principal |
| Target de cinematica inversa | `UR3_target` | Objeto que mueve el script Python |
| Tip de cinematica inversa | `UR3_tip` | Punto final que debe alcanzar el robot |
| Pinza paralela | `RG2` | Herramienta de agarre |
| Pieza | `pieza_pick` | Objeto que se recoge y transporta |
| Mesa elevada | `mesa_pick_place` | Superficie de trabajo elevada |

## Preparacion del UR3

1. Inserta el modelo `UR3` desde la biblioteca de modelos de CoppeliaSim.
2. Comprueba que existe el objeto `connection` en el extremo del robot.
3. Prepara la cinematica inversa como en el capitulo 19:
   - `UR3_tip` debe estar en el extremo del robot.
   - `UR3_target` debe ser hijo directo de `UR3`.
   - La configuracion IK debe usar `UR3_tip` como tip y `UR3_target` como target.
4. Antes de continuar, mueve manualmente `UR3_target` y comprueba que el robot sigue el movimiento.

## Montaje de la pinza RG2

La pinza debe ensamblarse con la herramienta de CoppeliaSim, no arrastrandola en el arbol.

1. Abre la biblioteca de modelos.
2. Ve a `Models > Components > Grippers > RG2`.
3. Arrastra `RG2` a la escena.
4. Selecciona el modelo `RG2`.
5. Manteniendo `Ctrl`, selecciona tambien el objeto `connection` del UR3.
6. Pulsa `Assemble / Disassemble`.
7. Inicia la simulacion y comprueba que la RG2 queda unida al extremo del robot.

## Posicion inicial del robot

Coloca el `UR3_target` en una posicion segura antes de ejecutar el script:

| Objeto | X | Y | Z |
|---|---:|---:|---:|
| `UR3_target` | `0.35` | `-0.05` | `0.38` |

Esta posicion deja el efector final elevado y alejado de la pieza antes de comenzar la maniobra.

## Pieza a recoger

Crea una pieza sencilla:

1. Menu `Add > Primitive shape > Cuboid`.
2. Cambia su nombre a `pieza_pick`.
3. Asigna un tamano aproximado de `0.04 x 0.04 x 0.04 m`.
4. Activa comportamiento dinamico si quieres probar agarre fisico real.
5. Colocala en la posicion de recogida.

| Objeto | X | Y | Z |
|---|---:|---:|---:|
| `pieza_pick` | `0.123` | `-0.197` | `0.281` |

La pieza queda sobre una plataforma fina cuya superficie esta aproximadamente en `Z = 0.261`.

## Zona de deposito

Puedes colocar una marca visual opcional para ver donde debe quedar la pieza.

1. Crea un cubo o cilindro muy fino.
2. Dale otro color para distinguirlo.
3. Desactiva su dinamica si solo lo usas como referencia visual.
4. Ponle un nombre como `zona_deposito`.

| Objeto | X | Y | Z |
|---|---:|---:|---:|
| `zona_deposito` | `0.113` | `-0.203` | `0.265` |

La pieza se depositara sobre esa zona. El script mueve la pinza hasta:

| Posicion del script | X | Y | Z |
|---|---:|---:|---:|
| `APROX_ORIGEN` | `0.25` | `-0.20` | `0.45` |
| `RECOGIDA` | `0.25` | `-0.20` | `0.35` |
| `APROX_DESTINO` | `0.20` | `-0.30` | `0.45` |
| `DEPOSITO` | `0.20` | `-0.30` | `0.35` |

## Resumen de posiciones iniciales

| Elemento | Nombre | X | Y | Z |
|---|---|---:|---:|---:|
| Robot | `UR3` | `0.00` | `0.00` | `0.00` |
| Mesa elevada | `mesa_pick_place` | `0.118` | `-0.200` | `0.241` |
| Target inicial | `UR3_target` | `0.25` | `-0.20` | `0.45` |
| Pieza | `pieza_pick` | `0.123` | `-0.197` | `0.281` |
| Zona destino | `zona_deposito` | `0.113` | `-0.203` | `0.265` |

## Recomendaciones de ajuste

- Si la pinza pasa por encima de la pieza sin agarrarla, baja ligeramente `RECOGIDA`.
- Si la pinza golpea la mesa, sube `RECOGIDA` y `DEPOSITO`.
- Si el desplazamiento horizontal queda demasiado cerca de los objetos, sube `APROX_ORIGEN` y `APROX_DESTINO`.
- Si la RG2 no responde, ejecuta primero `abrir_cerrar_rg2.py` para comprobar la pinza.
- Si la pieza no se mueve con la pinza, comprueba que se llama exactamente `pieza_pick`.

## Nombres que busca el script

El script es flexible, pero la configuracion recomendada es:

| Tipo | Nombre recomendado |
|---|---|
| Target del robot | `/UR3/UR3_target` |
| Pinza | `/UR3/connection/RG2` o `/RG2` |
| Pieza | `/pieza_pick` |
| Punto de agarre | `/UR3/connection/RG2/attachPoint` |

Con estos nombres no deberia ser necesario modificar el script Python.
