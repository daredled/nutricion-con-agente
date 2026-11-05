# Instrucciones para el agente

Plan de alimentación y seguimiento diario de una persona. Sirve para Claude Code o cualquier otro agente que lea este archivo.

Este archivo dice **cómo operar**: qué archivo es qué, la rutina diaria, la revisión semanal y lo técnico. No lleva datos de nadie. Antes de responder, lee también:
- `metodologia.md` (**con qué criterio**): rol de nutricionista deportivo, cómo se diseña, se sigue y se ajusta el plan, y cómo se estima el gasto.
- `persona/perfil.md` (**quién**): datos personales, salud, **reglas médicas no negociables**, entrenamiento, hábitos, alimentos permitidos y objetivo.
- `persona/operacion.md`: lo propio de esta persona al operar: plan vigente, fechas de revisión y decisiones.
- El plan vigente (**cifras**), en `persona/plan/`: línea base, pesos de referencia, hitos, menús y reglas de ajuste.

**Persona nueva:** si `persona/` no existe o está vacía, no hay plan que operar todavía. Seguir `crear-plan.md`, que parte por el filtro de seguridad. `ejemplo/` muestra una persona ficticia con todo armado.

## Base y datos personales
- **Base (compartible):** `AGENTS.md`, `CLAUDE.md`, `README.md`, `metodologia.md`, `crear-plan.md`, `formatos.md`, `plantillas/`, `visualizacion/`, `ejemplo/` (persona ficticia), `LICENSE` (MIT), `pyproject.toml` y `uv.lock`.
- **`persona/` (privado):** todo lo de la persona. **Nada personal va fuera de esta carpeta**, ni en el código: los valores que usa el panel van en `persona/config.toml`. Credenciales: `.env` en la raíz. Ambos están en `.gitignore`.
- Dentro de `persona/`, las rutas que mencionan los documentos (`registros/…`, `plan/…`, `analisis/…`) son relativas a esa carpeta.
- Si una regla aprendida sirve para cualquier persona, va en la base; si depende de esta persona, en `persona/`. Si existe, `COMPARTIR.md` dice lo que falta para compartir la base.

## Archivos clave
Todos dentro de `persona/`, salvo que se indique:
- `plan/AAAA-MM-DD_plan-faseN.md`: tiene los cálculos, los menús, las fechas y pesos de referencia, las reglas de ajuste y el paso a la fase siguiente.
- `plan/etiquetas/`: fotos de las tablas nutricionales (`producto.jpg`/`.png`), cada una con su transcripción `producto.md`. **Leer el `.md`, no la foto.** Cuando llegue una etiqueta nueva, guardarla con el nombre del producto y crear su `.md`.
- `analisis/gasto-calorico.md`: gasto real estimado contra el dispositivo y fórmulas MET por deporte, con la metodología para repetirlo. En cada recalibración se agrega un «Resultado N».
- `registros/seguimiento.md`: tabla diaria de tendencia y **registro de todos los cambios al plan**.
- `registros/AAAA-MM-DD.md` (+ `AAAA-MM-DD_fitdays.png` si el usuario manda la captura, + `AAAA-MM-DD_comida-N.png` por cada foto de comida fuera del plan): registro diario. La plantilla es `plantillas/registro.md` (en la base).
- **Fuentes de datos:** `[fuentes]` de `config.toml` dice de dónde sale cada dato (pesa, actividad, presión). Con Fitdays, WHOOP y Withings se usan los archivos de abajo; con otro dispositivo, `registros/pesa.csv`, `registros/actividad.csv` o `registros/presion.csv` en el formato de `formatos.md` (ver «Otros dispositivos»).
- `entrada/`: exportaciones de otros dispositivos, tal como las deja la persona. **No se editan.** `importar/`: el conversor de cada formato a los CSV estándar.
- `registros/fitdays.csv`: pesajes, una fila por pesaje, con los segmentos: filas manuales desde las capturas (`manual-AAAA-MM-DD`) o descargadas de la nube de Fitdays.
- `registros/whoop_diario.csv`: datos de WHOOP por día.
- `registros/whoop_ciclos.csv`: horas de cada ciclo de WHOOP, por día. Lo escribe `generar.py`.
- `registros/presion.csv`: presión arterial desde Withings, una fila por toma.
- `registros/ingesta.csv` (`date`, `kcal`, `nota`): ingesta estimada de los días que se salen de lo automático. El panel ya calcula solo el menú y las excepciones definidas en `config.toml` según los entrenamientos de WHOOP. Agregar una fila cuando haya comidas fuera del plan, snack de emergencia o ayuno. La nota es corta: sale en el tooltip.
- `imprimir/menu-refrigerador.html`: menú para el refrigerador (Carta horizontal). La persona lo abre en el navegador y lo imprime desde ahí; no se genera PDF. Incluye las compras de la semana: si cambia el menú, actualizarlas junto con la lista de compras del plan.
- `panel.html`: panel de seguimiento (peso, composición, presión, WHOOP). Se genera con `visualizacion/generar.py` desde `visualizacion/panel.template.html` (en la base) y `config.toml`; no editar `panel.html` a mano.
  - Arriba va el «Historial semanal»: un punto por lunes con el promedio de los 7 días que terminan ese día, en 5 filas (peso, masa muscular, músculo esquelético, masa grasa y % de grasa), desde el lunes que elija el botón «Desde», con «Reciente» (6 semanas) o «Total» (`weekly_history` en `generar.py`). El lunes que viene aparece con la semana en curso (promedio incompleto, punto hueco y línea punteada).
  - El gasto de WHOOP se muestra llevado a 24 h (`day_kcal` ÷ horas del ciclo × 24), porque cada ciclo dura de 19 a 29 h. Las horas salen de `whoop/raw/cycles.json` y se guardan en `registros/whoop_ciclos.csv`, que actualiza `generar.py` (el crudo solo trae la última ventana del sync). Al comentar el gasto de un día en los registros, usar también el valor por 24 h.
  - El gráfico de Energía muestra el gasto «fuera del entreno» y cada entrenamiento encima. WHOOP no distingue el basal de la actividad cotidiana, así que no se separan.
  - Un día suelto sin pesaje entre dos pesajes se dibuja como «estimado», con el promedio de ambos (`fill_gaps` en `generar.py`). Solo se muestra: no entra en los promedios de 7 días ni toca los CSV.
  - Los % del estándar por segmento no están en el CSV: `generar.py` los lee de `fitdays/raw/sync.json` (`*_bfr` grasa, `*_rom` músculo). En las filas manuales los lee de la tabla de segmentos del registro del día (copiada de la captura). Las figuras y los gráficos comparan contra la base que elija el botón del panel: el primer lunes con datos o el día 1 (el rango de fechas también parte ahí). `base_segmentos` de `config.toml` es solo el respaldo de los segmentos.

## Rutina diaria (cuando el usuario avisa de un pesaje nuevo)
Cada paso usa la fuente que diga `[fuentes]` de `config.toml`. Lo que sigue es el detalle de Fitdays, WHOOP y Withings; con otro dispositivo, en su lugar se convierte lo nuevo de `entrada/` (ver «Otros dispositivos») y se sigue igual.

1. **Pesa (`pesa = "fitdays"`): la fuente principal es la nube de Fitdays.** El usuario cierra sesión y vuelve a entrar en la app **antes de cada pesaje**, para que la app suba el pesaje a la nube. Para leerlo, `uv run fitdays-sync sync --login --csv persona/registros/fitdays.csv --raw-dir persona/fitdays/raw`. El `--login` está autorizado en la rutina diaria: desconecta la app, pero el usuario vuelve a entrar antes del pesaje siguiente.
   - Fitdays guarda una sola sesión por cuenta: entrar desde la herramienta desconecta la app del teléfono, y la app deja de subir los pesajes sin avisar hasta que el usuario vuelve a entrar (ver [Kinetrail](https://github.com/ErikaAlk/Kinetrail/blob/main/research/FITDAYSPLUS.md)). Nunca usar `--login` fuera de la rutina diaria.
   - **Respaldo:** si el pesaje no llega a la nube, pedir la captura del informe de la app. Guardarla como `persona/registros/AAAA-MM-DD_fitdays.png` (fecha de la "Hora de la prueba") y agregar la fila a mano a `fitdays.csv` con `data_id` = `manual-AAAA-MM-DD`. Si después llega desde la nube, borrar la fila manual (el CSV tiene fin de línea CRLF).
   - Si hay varios pesajes en el día, usar el de la mañana.
   - Un pesaje con la impedancia fallida trae la composición en 0 y una impedancia de ~5: no usarlo. Si hay uno válido ese día, usar ese.
   - Todo pesaje es en ayunas: no preguntar por la hora ni por el ayuno.
2. Pasar los datos de esa fila a `persona/registros/AAAA-MM-DD.md`, con la diferencia respecto del día anterior.
   - El CSV puede diferir de la app en ±0,1 kg en las masas por redondeo. Si hay captura, mandan los valores de la captura.
   - Pedir la cintura los lunes si no viene.
3. **Actividad (`actividad = "whoop"`):** `uv run whoop-sync sync --csv persona/registros/whoop_diario.csv --raw-dir persona/whoop/raw` y agregar al registro la recovery, la HRV, la FC en reposo, el sueño y los pasos del día anterior completo (columna `steps`, contra la meta del plan; también en la columna «Pasos día ant.» de `seguimiento.md`).
   - Revisar que el deporte de cada entrenamiento (columna `workouts`) calce con el horario del perfil. Si no calza (ej.: CrossFit registrado como `activity`, o un partido como otro deporte), sugerir al usuario que lo corrija en la app de WHOOP y volver a sincronizar después. El tipo de deporte cambia el strain y las kcal de la sesión, pero no el `day_kcal` del día.
   - **Presión (`presion = "withings"`):** `uv run withings-sync sync --csv persona/registros/presion.csv --raw-dir persona/withings/raw` y agregar al registro las tomas del día con su hora. En modo x3 (BPM Connect) cada fila ya es el promedio de 3 lecturas, así que no hay que promediar. Si hay más de una fila en el día, usar la de la mañana.
4. Si la ingesta del día anterior no fue la automática (fuera del plan, snack, ayuno), agregarla a `registros/ingesta.csv`. Agregar la fila a `registros/seguimiento.md` y calcular el promedio de 7 días del peso cuando haya 7 datos.
5. Comentar brevemente: la tendencia contra la tabla de pesos de referencia del plan y cualquier alerta del dispositivo o de presión.
   - **No ajustar el plan por el dato de un solo día.**
6. `uv run visualizacion/generar.py` **cada vez** que cambie el panel o sus datos. El panel queda solo en local (`persona/panel.html`): **no publicarlo en ningún servicio.**
   - Si cambian la ingesta del menú, los umbrales del plan o el factor de WHOOP (`whoopFactor`, gasto real = WHOOP × factor; se recalibra con cada «Resultado N» de `analisis/gasto-calorico.md`), actualizar `persona/config.toml`. La tabla de referencia se lee sola desde el plan.

## Otros dispositivos (`entrada/`)
La base se diseñó con WHOOP, Fitdays y Withings, pero cualquier dispositivo sirve si sus datos se pueden exportar: Garmin, Apple Watch (Apple Salud, en XML), Fitbit, Oura, Polar, otra pesa inteligente, una InBody o una planilla propia. El conversor los lleva a los CSV de `formatos.md`. Se aceptan con las mismas reglas que los soportados.
1. La persona deja la exportación en `persona/entrada/`, con la fecha en el nombre (ej.: `garmin-2026-11-04.csv`). Nunca se edita ni se borra: es el respaldo.
2. **Si ya tiene las columnas de `formatos.md`**, se copia tal cual a `registros/`. **Si no**, la primera vez se escribe un conversor en `persona/importar/<dispositivo>.py` (modelo: `ejemplo/importar/garmin.py`) y se anota en `operacion.md`; las veces siguientes basta con `uv run persona/importar/<dispositivo>.py`.
   - El conversor solo cambia nombres, unidades y formatos. No inventa datos: lo que el dispositivo no mide queda vacío.
   - Antes de usarlo, revisar con la persona algunas filas contra lo que muestra la app del dispositivo (fechas, unidades, que el sueño sea el de la noche anterior).
3. Declarar la fuente en `[fuentes]` de `config.toml` (`csv`, `manual` o `ninguna`) y el nombre en `dispositivo`, que es el que muestra el panel.
4. Reglas para datos de otra fuente (ver «Fuentes de datos» en `metodologia.md`): factor de gasto propio desde 1,0, umbrales desde su propio promedio, y las reglas que usan un dato que no existe (ej.: la recovery) no se aplican; se anota en el plan.
5. Si la persona cambia de dispositivo a mitad del plan, se anota la fecha en `operacion.md` y se recalibra el factor de gasto con el nuevo: los valores de dos dispositivos no se comparan entre sí.

## Comidas fuera del plan (fotos)
Cada vez que el usuario se sale del plan manda fotos de lo que comió. Por cada foto:
1. Guardarla como `persona/registros/AAAA-MM-DD_comida-N.png` (fecha del día en que se comió; N = 1, 2… en orden). Lo que se come de madrugada (antes de dormir, ej.: 01:00) cuenta en el día anterior.
2. Estimar kcal, macros y **sodio**, diciendo los supuestos (porción, aceite, salsas). Si algo no se ve (cantidad comida, bebida, salsa), preguntar solo eso.
3. Anotarlo en el registro de ese día (crear el archivo si no existe) y poner el total del día en `registros/ingesta.csv`.
4. Si es durante el día, decir cómo seguir el resto del día **sin restringir de más** (sodio incluido). Nunca compensar al día siguiente.

## Revisión semanal (lunes, con el pesaje de ese día)
- Aplicar las reglas de ajuste del plan usando el promedio de 7 días y los datos de WHOOP.
- Si hay cambios:
  - Actualizar el plan con una nueva versión y anotarla en el encabezado.
  - Registrar el cambio en `registros/seguimiento.md`.
  - Regenerar el menú del refrigerador (ver abajo).
- Las revisiones clave y los hitos de esta persona, con sus fechas, están en `persona/operacion.md`.

## Técnico
- Python **solo con `uv run`** (venv `.venv`, Python 3.14). Nunca `python3`.
- **Preparar el entorno lo hace el agente, no la persona:** si `.venv` no existe (primera vez o recién copiada la carpeta), correr `uv sync` antes de cualquier otra cosa. Lo único que se le pide a la persona es tener uv instalado; si no lo tiene, darle el enlace de instalación (docs.astral.sh/uv).
- WHOOP: paquete `whoop-sync` (repo público github.com/daredled/whoop-sync, instalado desde GitHub; para actualizarlo: `uv lock --upgrade-package whoop-sync && uv sync`). Credenciales en `.env`, tokens en `~/.config/whoop-sync/tokens.json`. Nunca mostrarlos.
  - Las columnas del CSV están en inglés (`date`, `recovery`, `hrv_ms`, `resting_hr`, `sleep_h`, `day_kcal`, `steps`, `workouts`…). Exporta todo lo que da la API v2: fases del sueño (`light_h`, `deep_h`, `rem_h`, `awake_h`), necesidad y deuda de sueño, siestas, FC máxima, minutos por zona de FC de los entrenamientos (`zone0_min`…`zone5_min`). Ver el README del paquete.
  - **Cada fila es un ciclo, no un día calendario.** El ciclo va de dormirse a dormirse (19 a 29 h) y lleva la fecha del día en que está despierto (inicio local + 12 h).
    - La recovery, la HRV, la FC en reposo y el sueño son de la noche que termina esa mañana. El gasto, el strain, los pasos y los entrenamientos son del resto del ciclo. Por eso, en el registro de hoy, la noche sale de la fila de hoy, y el gasto, los pasos y los entrenamientos, de la fila de ayer (la de hoy sigue abierta).
    - El gasto se lee llevado a 24 h (ver el panel, arriba). Los pasos no se ajustan: dependen en parte de la duración del ciclo.
    - La comida de madrugada, antes de dormirse, cuenta en el día anterior, igual que el ciclo. El pesaje de la mañana refleja el ciclo anterior.
    - Casos raros: un sueño principal que parte después del mediodía deja el ciclo con la fecha siguiente, y los entrenamientos usan la fecha en que empiezan, no la del ciclo.
  - Si el token se invalida, el usuario debe correr `uv run whoop-sync auth` en una terminal aparte.
- Withings (presión): paquete `withings-sync` (repo público github.com/daredled/withings-sync, instalado desde GitHub; para actualizarlo: `uv lock --upgrade-package withings-sync && uv sync`). Credenciales `WITHINGS_*` en `.env`, tokens en `~/.config/withings-sync/tokens.json`. Nunca mostrarlos.
  - Columnas del CSV: `date`, `time`, `systolic`, `diastolic`, `pulse`, `grpid`, `timezone`. La hora es local.
  - Si el token se invalida, el usuario debe correr `uv run withings-sync auth` en una terminal aparte.
- Fitdays (pesa): paquete `fitdays-sync` (repo público github.com/daredled/fitdays-sync, instalado desde GitHub; para actualizarlo: `uv lock --upgrade-package fitdays-sync && uv sync`). **Experimental:** API no oficial (protocolo de la app Android). Credenciales `FITDAYS_EMAIL`/`FITDAYS_PASSWORD` en `.env`, sesión en `~/.config/fitdays-sync/session.json`. Nunca mostrarlas.
  - Nunca hace login sola: `sync` usa la sesión guardada y, si no sirve, se detiene; `--login` entra y desconecta la app del teléfono. Si responde código 11000 ("cuenta o contraseña incorrecta"), el usuario debe revisar la contraseña en la app y actualizar `.env`.
  - Columnas del CSV: `date`, `time`, `weight_kg`, `body_fat_pct`, `fat_mass_kg`, `fat_free_mass_kg` (= músculo + hueso, como la app), `muscle_kg`, `skeletal_muscle_kg`, `protein_kg`, `water_kg`, `bone_kg`, `subcutaneous_fat_pct`, `visceral_fat`, `bmr`, `body_age`, `score`, `whr`, segmentos `fat_*_kg` y `muscle_*_kg` (`left_arm`, `right_arm`, `trunk`, `left_leg`, `right_leg`)…
  - Si la cuenta tiene varios perfiles (`suid`), `fitdays.suid` de `config.toml` dice cuál es el de esta persona.
- Menú impreso: el HTML debe caber en 1 página Carta horizontal al imprimirlo desde el navegador (sin encabezados ni pies de página). Queda solo en local.
- **Otros dispositivos o carga manual:** basta con escribir los mismos CSV. Las columnas que necesita el panel están en `formatos.md`.
- **Otra carpeta de persona:** `uv run visualizacion/generar.py ejemplo` genera el panel de `ejemplo/` (o de cualquier carpeta con la misma estructura).
