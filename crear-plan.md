# Crear el plan de una persona nueva

Cómo pasar de la base a un plan en marcha. Se usa cuando `persona/` no existe o está vacía. Los criterios están en `metodologia.md`; la operación diaria, en `AGENTS.md`. Para ver cómo queda todo armado, mirar `ejemplo/` (persona ficticia).

Si `.venv` no existe, el agente corre `uv sync` primero (ver «Técnico» en `AGENTS.md`).

Orden: **seguridad → entrevista → datos → cálculos y plan → semana 0 → línea base y archivos.** No pasar al siguiente paso sin cerrar el anterior. Los pasos están numerados por tema; el plan se arma antes de la semana 0, que ya lo usa.

## 1. Filtro de seguridad (antes de cualquier cálculo)
Un déficit no es para todos. Preguntar, antes que nada:
- Edad. **Menores de 18:** no armar un déficit; derivar a un profesional.
- **Embarazo o lactancia:** no armar un déficit.
- **Trastornos de la conducta alimentaria**, actuales o pasados (anorexia, bulimia, atracones): no armar un déficit sin su equipo tratante.
- **Diabetes**, sobre todo con insulina o sulfonilureas (riesgo de hipoglicemia al bajar los carbohidratos).
- **Enfermedad renal** (cambia la proteína y el potasio que se pueden usar), **hepática** o **cardíaca**.
- Hipertensión, cirugías recientes, lesiones y cualquier otra condición en tratamiento.
- **Todos los medicamentos y suplementos**, con su dosis.
- IMC bajo 18,5: no hay déficit que armar.

**Si hay alguna condición de la lista, el plan se arma solo con el visto bueno de su médico.** Decirlo claro y no seguir hasta que lo tenga.

Por cada condición y cada medicamento, buscar qué implica para la dieta y anotarlo como **regla médica no negociable** en `persona/perfil.md`, para que la confirme con su médico. Ejemplos:
- **ARA-II, IECA o diuréticos ahorradores de potasio:** nunca sal light ni sustitutos con cloruro de potasio, ni suplementos de potasio; vigilar el potasio del menú.
- **Hipertensión:** límite de sodio (≤2.000 mg/día es una referencia común), sal agregada pesada; cuidado con los antiinflamatorios (AINEs) y la cafeína.
- **Anticoagulantes como la warfarina:** vitamina K estable de un día a otro.
- **Bloqueadores de canales de calcio:** evitar el pomelo.

Además, en el perfil: cuándo derivar al médico (umbrales de presión, glicemia, síntomas) y si la persona quiere o no que se le pidan exámenes. **El agente no reemplaza al médico:** ante una duda de salud, deriva.

## 2. Entrevista
Llenar `persona/perfil.md` (desde `plantillas/perfil.md`):
- Datos: sexo, edad, estatura, trabajo, actividad fuera del entrenamiento.
- Intolerancias, alergias, alcohol, café.
- Entrenamiento: días, horas, duración e intensidad de cada actividad.
- Hábitos: horarios de comida, hambre, ansiedad, lo que suele sacarle del plan.
- **Alimentos permitidos:** solo los que de verdad va a comer y cocinar. El menú se arma solo con ellos.
- Objetivo de la fase 1 (meta de % de grasa, cintura u otra) y un ritmo aceptable.

## 3. Dispositivos y datos
- Preguntar qué usa para pesarse, para la actividad y el sueño, y para la presión, y declararlo en `[fuentes]` de `config.toml`. WHOOP, Fitdays y Withings tienen sincronización; cualquier otro sirve dejando su exportación (CSV, XML…) en `persona/entrada/` (ver «Otros dispositivos» en `AGENTS.md`).
- Con los soportados: copiar `.env` con las credenciales de cada uno (ver `README.md`) y autorizar.
- Bajar el historial que haya: si el dispositivo tiene 2 a 5 semanas previas, sirven para el gasto inicial y para la referencia de HRV, FC en reposo y sueño (promedio y desviación estándar, sin semanas de descanso o enfermedad).
- Sin dispositivo de actividad (`actividad = "ninguna"`): se sigue solo con la pesa; el gasto sale de las fórmulas y se calibra con el peso.
- Un pesaje inicial completo (con composición, si la pesa la da), la cintura y las etiquetas de los productos envasados del menú (whey, pan…), con su transcripción en `plan/etiquetas/`.

## 4. Semana 0 (adaptación)
- Se arma el plan (pasos 5 y 6) con los datos previos y la semana 0 ya usa su menú: así la ingesta de esa semana es conocida. `ingesta.menu` parte el primer día de la semana 0.
- La primera semana es de **adaptación**: se pesa todos los días, se ajusta lo que no funcione del menú y no se juzga el ritmo.
- El peso baja más rápido por agua y glucógeno (y por cambios de sal). No cuenta para los ajustes.
- **Línea base = promedio de los 7 pesajes de la semana 0** (lunes a domingo), también para la composición. El **día 1** es el lunes siguiente. Al terminar la semana 0 se fijan con ella la tabla de pesos de referencia y los hitos.
  - El «Historial semanal» del panel promedia los 7 días que terminan cada lunes (martes a lunes), así que su punto del día 1 puede diferir un poco de la línea base.

## 5. Cálculos
### Gasto
- **Dispositivo:** promedio diario de las semanas previas, llevado a 24 h si es WHOOP. Empezar con **factor × 1,0** (`whoopFactor = 1` en `config.toml`): no copiar el factor de otra persona.
- **Fórmulas:** basal (Katch-McArdle con la masa libre de grasa o Mifflin-St Jeor) × factor de actividad, o basal × 1,2 + METs del Compendio por sesión (ver `plantillas/gasto-calorico.md`). Las fórmulas con factor de actividad tienden a sobreestimar.
- **Gasto de trabajo:** un valor intermedio entre el dispositivo y las fórmulas (MET del Compendio corregidas por el basal, mejor que el basal × 1,55–1,725), con su rango. Ante la duda, el más bajo, siempre que el déficit contra el borde alto del rango no pase del 30 %. Se corrige a las 2 semanas con la tendencia del peso: ese es el dato que manda.

### Déficit y macros
- **Déficit:** 20–25 % del gasto de trabajo. No más: los déficits grandes terminan en atracones.
- **Ritmo:** déficit diario × 7 ÷ 7.700 kg por semana; idealmente 0,5–1 % del peso por semana.
- **Proteína:** 1,6–2,2 g/kg de peso (o 2,3–3,1 g/kg de masa libre de grasa en un déficit con entrenamiento de fuerza). Con enfermedad renal, lo que diga su médico.
- **Grasa:** 20–30 % de las calorías; no bajar de ~0,6 g/kg.
- **Carbohidratos:** el resto, concentrados alrededor del entrenamiento.
- **Fibra** ≥25–30 g; **sodio** según su regla médica o el límite general.
- **Límite inferior:** no bajar del basal estimado sin revisar todo el plan.

### Según la persona
- **Mujeres:** el peso sube 1–2 kg de agua en algunas fases del ciclo menstrual. Comparar la tendencia de un ciclo con el siguiente y no ajustar por una semana alta. La pérdida de la menstruación es motivo para derivar.
- **Intolerancia a la lactosa u otras exclusiones:** revisar el calcio (~1.000 mg/día) y lo que falte, y proponer cómo cubrirlo.
- **Alcohol:** se estima y se anota como comida fuera del plan (7 kcal/g), sin compensar al día siguiente.
- **Sin tensiómetro:** la presión es opcional; en `config.toml` quedan los umbrales generales.

### Metas y trayectoria
- **Peso objetivo:** masa libre de grasa ÷ (1 − meta de grasa), con y sin perder el 10–20 % de lo bajado como masa libre de grasa. Es un rango; el criterio real es el % de grasa y la cintura.
- **Pesos de referencia:** desde la línea base, el ritmo central por semana, hasta la zona meta.
- **Ritmo objetivo:** el rango que la persona aceptó en el perfil, sin pasar del 1 % del peso por semana. Las reglas de ajuste del plan usan ese rango.
- **Hitos de 7, 15, 30, 60 y 90 días** (el hito de N días cae en el día 1 + N − 1) sobre esa trayectoria, con «va bien si queda bajo» = referencia + 1 kg, y metas de masa libre de grasa (línea base − ~1 kg), cintura (~1 cm por kg), menú (≥90 %) y pasos.

## 6. El plan
Escribirlo en `persona/plan/AAAA-MM-DD_plan-fase1.md` (fecha de creación) desde `plantillas/plan.md`, **respetando el formato de las tablas** que lee el panel. Debe tener todo lo que pide `metodologia.md` («Diseño del plan»):
- Cálculos con sus supuestos y las fuentes.
- Menú con gramos exactos (crudo o cocido), kcal, macros y sal por comida, según su horario de entrenamiento. **Un solo menú por tipo de día** es más fácil de cumplir.
- Excepciones: día sin entrenamiento (menú completo + caminata, sin recorte), doble turno o sesión muy intensa (más comida), y el **snack de emergencia en 2 pasos**.
- Intercambios por gramo dentro de cada grupo.
- Reglas médicas aplicadas al menú.
- Qué mandar y cada cuánto, reglas de ajuste, pausa en mantención y transición a la fase 2.
- Lista de compras semanal.

Antes de dárselo a la persona, revisar las sumas de cada comida y del día, el sodio y lo que pidan sus reglas médicas (potasio, cafeína…).

## 7. Archivos
Crear `persona/` con:
- `config.toml` (desde `plantillas/config.toml`): fechas, menú, umbrales de las reglas, entrenamientos del dispositivo y `whoopFactor = 1`.
- `perfil.md` y `operacion.md` (fechas de revisión: día 1, hitos, recalibración a las 2 semanas, pausa en mantención).
- `plan/` con el plan y `plan/etiquetas/` para las tablas nutricionales.
- `registros/seguimiento.md` (desde `plantillas/seguimiento.md`) y los CSV que vaya escribiendo cada dispositivo.
- `analisis/gasto-calorico.md` (desde `plantillas/gasto-calorico.md`).
- `imprimir/menu-refrigerador.html` (desde `plantillas/menu-refrigerador.html`), para imprimirlo desde el navegador.

Después: `uv run visualizacion/generar.py` y revisar el panel. Desde ahí, la rutina diaria de `AGENTS.md`.

## 8. Primeras revisiones
- **Semana 2 (día 15):** primera recalibración del gasto con la tendencia del peso (`analisis/gasto-calorico.md`, «Resultado 1») y primera evaluación de las reglas de ajuste. Actualizar `whoopFactor`.
- **Referencias del dispositivo:** sin historial, el umbral de HRV parte provisorio (promedio − 1 DE de las noches que haya, al menos 7) y se fija con las primeras 3 a 4 semanas.
- Cada cambio sube la versión del plan y se anota en `seguimiento.md`.
