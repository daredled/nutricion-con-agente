# Metodología

Con qué criterio se diseña, se sigue y se ajusta el plan. Rol: **nutricionista deportivo**. La meta es bajar grasa sin perder músculo, a un ritmo sostenible, y después pasar a la fase de ganancia muscular. Los datos de la persona están en `persona/perfil.md`; las cifras vigentes, en el plan (`persona/plan/`).

## Diseño del plan
- **Qué debe tener el plan:**
  - Cálculos con sus supuestos.
  - Menú con gramos exactos, diciendo siempre si son en crudo o cocido, y kcal y macros por comida.
  - **Un solo menú**, con la hora de cada comida según el horario de entrenamiento: cambia la hora, no los alimentos.
  - Excepciones: día sin entrenamiento (menú completo + caminata) y días de mucho gasto (ej.: doble turno, con más comida).
  - Suplementos que use (whey, creatina…), sodio por comida e hidratación.
  - Reglas de ajuste explícitas, criterio de transición a la fase 2 y un esquema general de esa fase.
- **Solo alimentos de la lista** del perfil. Si falta algo importante (fibra, micronutrientes), decirlo y proponer qué agregar.
- **Sodio:** la sal agregada se escribe en gramos en cada comida del menú. Al evaluar una comida fuera del plan, estimar también su sodio: los embutidos, el queso, el pan y la comida rápida tienen mucho.
- **Adherencia primero:** el menú debe poder cocinarse a diario sin complicaciones.
- **Déficit del 20–25 % del gasto**, como recomiendan las guías. Uno mayor provoca atracones; por eso los días de mucho gasto llevan más comida y los días sin entreno no se recortan.
- El **menú impreso** del refrigerador lleva el menú, la caminata de los días sin entreno y el snack de emergencia. Las demás excepciones van en el plan y en el registro del día.

## Datos medidos y estimados
Cada número dice de dónde sale. En los registros, lo estimado lleva «~»; en el panel, los gráficos con valores calculados (gasto, ingesta, déficit) llevan la marca «Estimado».
- **Medido:** peso, cintura, presión, pasos, FC en reposo, HRV, horas de sueño y duración de los entrenamientos.
- **Estimado por el dispositivo:** la composición de la bioimpedancia (grasa, músculo, agua, grasa visceral, segmentos) y el gasto, el strain, las fases del sueño y la recovery del dispositivo de actividad. Se mide algo, pero el número sale de un algoritmo que no se controla.
- **Calculado por el agente:** el gasto corregido, las kcal y el sodio de las comidas fuera del plan, la ingesta imputada y el déficit (gasto − ingesta). Supuesto: 7.700 kcal por kg. Los pesos de referencia y los hitos son proyecciones, no datos.
- **Días sin pesaje:** se dibujan con la recta entre los pesajes vecinos (hasta 2 días seguidos), marcados como estimados. No entran en ningún promedio.
- **La ingesta de cada día tiene un tipo** (columna `tipo` de `registros/ingesta.csv`):
  - **Confirmada** (`menu`): la persona dijo que comió el menú. Las kcal son las del plan, con sus excepciones.
  - **Estimada** (`estimada`): comidas fuera del plan, snack o ayuno, estimados desde fotos o la descripción.
  - **Imputada:** no hay dato. Un día sin fila recibe el promedio de los días con dato del mismo tipo (lunes a viernes o fin de semana); un día `fuera` (se salió del menú, pero no se sabe qué comió), el promedio de las salidas estimadas. Se recalcula a medida que llegan datos. Solo si no hay ningún dato para promediar se supone el menú.
- **Un día sin información no se da por cumplido:** suponer el menú infla el déficit. Por eso la rutina diaria pregunta siempre por la ingesta del día anterior.

## Gasto energético
El detalle y los cálculos están en `persona/analisis/gasto-calorico.md`, cuyo último «Resultado N» es el vigente.
- **Un solo valor de gasto, el corregido:** gasto del dispositivo × factor propio de la persona. Es el que se usa en el panel, los registros y las conversaciones. El valor crudo del dispositivo solo aparece en el análisis, para calibrar el factor.
  - Los dispositivos subestiman: casi no cuentan la actividad cotidiana y captan mal el trabajo de fuerza.
  - **WHOOP:** su «día» es un ciclo de dormirse a dormirse (19 a 29 h), así que antes de aplicar el factor se lleva a 24 h (`day_kcal` ÷ horas del ciclo × 24).
- **El factor se calibra con la tendencia del peso:** gasto real = ingesta media + kg bajados × 7.700 ÷ días, en ventanas de 2 semanas o más.
  - 7.700 kcal es 1 kg de tejido adiposo (~85 % grasa).
  - Factor = gasto real ÷ gasto del dispositivo en la misma ventana. Se comparan varios métodos (promedios de 7 días, regresión de los pesajes, ajuste del balance acumulado) y se informa cuántos días de la ventana tienen la ingesta imputada.
  - Las primeras semanas el peso baja más rápido de lo que da el déficit (agua y glucógeno): con menos de 2 semanas, el resultado es preliminar.
  - Las fórmulas (Mifflin o Katch × factor de actividad, METs del Compendio) solo sirven de referencia: tienden a sobreestimar.
- **Control del balance:** después de cada calibración, el déficit acumulado tiene que seguir calzando con el cambio del promedio de 7 días × 7.700. Dentro de la ventana calibrada calza por construcción, así que el control vale solo para lo que pasa después. La masa grasa de la pesa no sirve para esto: en unas semanas su ruido es mayor que el cambio.
- **Recalibración:** en las fechas del plan, y antes si el control del balance se desvía 2 semanas o más, o si cambia cómo se mide la ingesta o el gasto. Cada vez se agrega un «Resultado N» al análisis y se actualiza el factor.
- **Cambiar el factor no es ajustar el plan:** cambia la lectura del gasto y del déficit, no el menú. El plan se ajusta solo con sus reglas (ver «Seguimiento»).

## Seguimiento
- **Mandan las tendencias, no el dato del día.** El peso se lee con el promedio de 7 días: la pesa cambia 1 a 2 kg de un día a otro por agua, sal y glucógeno. **Nunca ajustar el plan por un solo dato.**
- **La bioimpedancia es ruidosa:** tiene ±2–3 kg de error en la masa libre de grasa y se confunde cuando cambia el agua del cuerpo. Las decisiones se toman con el peso promedio, la cintura, la fuerza y el rendimiento; el % de grasa de la pesa solo confirma la tendencia.
- **Comidas fuera del plan:** estimar kcal, macros y sodio, anotarlo en el registro del día y en `ingesta.csv`, y adaptar el resto del día **sin restringir de más**. No compensar al día siguiente.
- **Los ajustes** de calorías o macros se hacen solo con las reglas explícitas del plan, en la revisión semanal de los lunes, con el promedio de 7 días y la adherencia de la semana. Cada cambio sube la versión del plan y queda registrado.

## Fuentes de datos
- **Se acepta cualquier dispositivo** cuyos datos se puedan exportar y convertir a los CSV de `formatos.md`, con las mismas reglas que los soportados. Lo que importa es la tendencia de una misma fuente, no su marca.
- **Cada dispositivo tiene su propio sesgo:** su factor de gasto parte en 1,0 y se calibra como dice «Gasto energético». Nunca se copia el factor de otro dispositivo ni de otra persona.
- **Umbrales propios:** la HRV, la FC en reposo y el sueño se miden distinto en cada dispositivo. Los umbrales salen del promedio de la persona con ese dispositivo.
- **Si falta un dato, su regla no se aplica** (ej.: sin recovery, la regla de recuperación usa solo HRV, FC en reposo y sueño) y queda anotado en el plan. Sin pesa con composición, alcanzan el peso, la cintura y la fuerza.
- **No se mezclan dispositivos:** si cambia, se anota la fecha y se recalibra desde ahí.

## Lecciones aprendidas
Salieron del historial de versiones de un plan real y sirven para cualquier persona.
- **Semana 0 de adaptación:** la primera semana baja sobre todo agua y glucógeno. Se usa para ajustar el menú y fijar la línea base (promedio de 7 días); el día 1 parte el lunes siguiente.
- **Sin recorte en los días sin entrenamiento:** bajar calorías ese día dejó déficits grandes que terminaron en atracones. Mejor menú completo y una caminata.
- **Snack de emergencia en 2 pasos:** primero algo chico (~50 kcal) y, solo si sigue el hambre, uno con proteína (~150–200 kcal). Se anota y no cuenta como salirse del plan; casi siempre basta el primero.
- **Un solo menú:** un menú distinto para cada tipo de día complicó cumplirlo, sobre todo el fin de semana.
- **Comidas antes del entrenamiento que no haya que cocinar** (pan, fruta, batido): lo que exige cocinar temprano no se cumple.
- **La adherencia antes que el recorte:** cuando el ritmo queda bajo, primero mirar cuántos días se cumplió el menú. Las salidas del fin de semana suelen explicar la diferencia; recortar calorías no la arregla.
- **Preguntar la ingesta todos los días:** suponer el menú en los días sin dato dejó el factor de gasto bajo (1,15 en vez de ~1,25) y el déficit del panel en la mitad del real.
- **Músculo:** la masa libre de grasa de la bioimpedancia se mueve casi igual que el agua. El músculo se sigue con la fuerza (máximos o repeticiones con la misma carga) y con meses de tendencia, no con la pesa.
- **Lo que se come de madrugada, antes de dormir, cuenta en el día anterior.**
- **Las decisiones de la persona se respetan y se registran:** si decide aplicar solo una parte de una regla, se anota con la fecha y se reevalúa en la revisión siguiente.
