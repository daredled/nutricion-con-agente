# Formatos de los datos

Qué archivos lee el panel (`visualizacion/generar.py`) y con qué columnas. Sirven para cargar datos a mano o desde cualquier dispositivo: basta con producir el mismo CSV. Todos van en `persona/registros/`, con encabezado, fechas `AAAA-MM-DD`, horas `HH:MM` locales y punto decimal. Una columna que falta o una celda vacía cuenta como «sin dato».

## Fuentes
`[fuentes]` de `config.toml` dice de dónde sale cada dato y qué archivo lee el panel:

| Dato | Fuente | Archivo |
|---|---|---|
| `pesa` | `fitdays` (por defecto) | `fitdays.csv` |
| | `csv`: otra pesa | `pesa.csv` |
| | `manual`: peso anotado en `seguimiento.md` | — |
| `actividad` | `whoop` (por defecto) | `whoop_diario.csv` |
| | `csv`: otro dispositivo | `actividad.csv` |
| | `ninguna` | — |
| `presion` | `withings` (por defecto), `csv` o `ninguna` | `presion.csv` |

`dispositivo` es el nombre que muestra el panel (ej.: `"Garmin"`). Las exportaciones originales van en `persona/entrada/` y sus conversores en `persona/importar/` (ver «Otros dispositivos» en `AGENTS.md`; modelo: `ejemplo/importar/garmin.py`). El panel oculta las secciones que no tienen datos.

## Pesa: `fitdays.csv` o `pesa.csv`
`fitdays.csv` lo escribe `fitdays-sync`; `pesa.csv` va con las mismas columnas. Una fila por pesaje; si hay varios en un día, el panel usa el primero (el de la mañana).

| Columna | Obligatoria | Qué es |
|---|---|---|
| `date`, `time` | sí | Fecha y hora del pesaje |
| `weight_kg` | sí | Peso |
| `body_fat_pct`, `fat_mass_kg`, `fat_free_mass_kg` | recomendadas | Grasa y masa libre de grasa |
| `muscle_kg`, `skeletal_muscle_kg`, `visceral_fat` | opcionales | Músculo y grasa visceral |
| `fat_{segmento}_kg`, `muscle_{segmento}_kg` | opcionales | Segmentos: `left_arm`, `right_arm`, `trunk`, `left_leg`, `right_leg` |
| `suid` | opcional | Perfil de la cuenta, si tiene varios (`fitdays.suid` de `config.toml`) |
| `data_id` | opcional | Id del pesaje; `manual-AAAA-MM-DD` para las filas a mano |

`fitdays-sync` exporta más columnas (agua, proteína, TMB, edad corporal…); el panel no las necesita.

**Otra pesa:** `pesa.csv` con `date`, `time`, `weight_kg` y lo que dé la pesa. **Sin pesa inteligente** (`pesa = "manual"`): el peso se anota en `seguimiento.md` (columna «Peso») y el panel lo toma de ahí.

## Actividad y sueño: `whoop_diario.csv` o `actividad.csv`
`whoop_diario.csv` lo escribe `whoop-sync`, con **una fila por ciclo de WHOOP**, no por día calendario (ver `AGENTS.md`). `actividad.csv` va con las mismas columnas y una fila por día calendario.

| Columna | Qué es |
|---|---|
| `date` | Fecha del ciclo |
| `recovery`, `hrv_ms`, `resting_hr`, `sleep_h` | La noche que termina esa mañana |
| `day_kcal`, `day_strain`, `steps` | Gasto, carga y pasos del ciclo |
| `workouts` | Entrenamientos: `tipo NNmin NNkcal` (y opcionalmente `strain N.N`), separados por ` \| `. El `tipo` se nombra en `[[entrenamientos]]` de `config.toml` |
| `cycle_complete` | `yes` si el ciclo terminó |

Las horas de cada ciclo, para llevar el gasto a 24 h, salen de `whoop/raw/cycles.json` y se guardan en `whoop_ciclos.csv` (`date`, `cycle_h`).

**Otro dispositivo (Garmin, Apple, Oura, Fitbit…):** `actividad.csv`, con `cycle_complete = yes` para los días cerrados. El gasto se toma tal cual, como de 24 h. Lo que el dispositivo no mida queda vacío (sin `recovery`, el panel muestra solo la HRV). Su factor de gasto se calibra desde 1,0, igual que el de WHOOP (`plantillas/gasto-calorico.md`); en `config.toml` se llama `whoopFactor` por historia, pero vale para cualquier dispositivo.

## Presión: `presion.csv` (opcional)
Lo escribe `withings-sync` o un conversor (`presion = "csv"`). Columnas: `date`, `time`, `systolic`, `diastolic`, `pulse` (más `grpid` y `timezone`, que el panel no usa). A mano: una fila por toma.

## Ingesta: `ingesta.csv`
`date`, `kcal`, `nota`. Solo los días que no fueron el menú (comidas fuera del plan, snack, ayuno). El resto lo calcula el panel con `ingesta.menu` de `config.toml`.

## Seguimiento: `seguimiento.md`
Tabla diaria (ver `plantillas/seguimiento.md`). El panel lee de ahí el peso, la grasa, la masa libre de grasa y la grasa visceral de los días que no están en el CSV de la pesa.

## Plan
`generar.py` lee del plan vigente las versiones, la tabla «Pesos de referencia» y la tabla «Hitos». El formato está en `plantillas/plan.md`.
