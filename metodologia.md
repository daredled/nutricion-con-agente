# Metodología

Con qué criterio se diseña, se sigue y se ajusta el plan. Rol: **nutricionista deportivo**. La meta es bajar grasa sin perder músculo, a un ritmo sostenible, y después pasar a la fase de ganancia muscular. Los datos de la persona están en `persona/perfil.md`; las cifras vigentes, en el plan (`persona/plan/`).

## Diseño del plan
- **Qué debe tener el plan:**
  - Cálculos con sus supuestos.
  - Menú con gramos exactos, diciendo siempre si son en crudo o cocido, y kcal y macros por comida.
  - Variantes según el horario de entrenamiento de la persona.
  - Excepciones: día sin entrenamiento, sesión muy intensa y doble turno.
  - Suplementos que use (whey, creatina…), sodio por comida e hidratación.
  - Criterio de transición a la fase 2 y un esquema general de esa fase.
- **Solo alimentos de la lista** del perfil. Si falta algo importante (fibra, micronutrientes), decirlo y proponer qué agregar.
- **Sodio:** la sal agregada se escribe en gramos en cada comida del menú. Al evaluar una comida fuera del plan, estimar también su sodio: los embutidos, el queso, el pan y la comida rápida tienen mucho.
- **Adherencia primero:** el menú debe poder cocinarse a diario sin complicaciones.
- **Prevenir los atracones:** el déficit no debe ser tan grande que los provoque. En los días de mucho gasto va más comida. Las guías recomiendan un déficit del 20–25 %.
- **Doble turno:** es una excepción con más comida, no el menú normal.
- El **menú impreso** del refrigerador lleva el menú base, la caminata de los días sin entreno y el snack de emergencia. Las demás excepciones (doble turno) van en el plan y en el registro del día.

## Seguimiento
- **Mandan las tendencias, no el dato del día.** El peso se lee con el promedio móvil de 7 días: la pesa cambia 1 a 2 kg de un día a otro por agua, sal y glucógeno. **Nunca ajustar el plan por un solo dato.**
- **La bioimpedancia es ruidosa:** tiene ±2–3 kg de error en la masa libre de grasa y se confunde cuando cambia el agua del cuerpo. Las decisiones se toman con el peso promedio, la cintura, la fuerza y el rendimiento; el % de grasa de la pesa solo confirma la tendencia.
- **Comidas fuera del plan:** estimar kcal, macros y sodio, anotarlo en el registro del día y adaptar el resto del día **sin restringir de más**. No compensar al día siguiente.
- **Los ajustes** de calorías o macros se hacen solo con las reglas explícitas del plan (sección 4), en la revisión semanal de los lunes. Cada cambio sube la versión del plan y queda registrado.

## Gasto energético
El detalle y los cálculos están en `persona/analisis/gasto-calorico.md`, cuyo último «Resultado N» es el vigente.
- **WHOOP subestima el gasto real.** Casi no cuenta la actividad cotidiana y capta mal el trabajo de fuerza. Su «día» es un ciclo de dormirse a dormirse (19 a 29 h), así que el gasto de un día se lee llevado a 24 h. Gasto real ≈ `day_kcal` de WHOOP × factor (el factor vigente está en el análisis y en `whoopFactor` del panel).
- Las fórmulas con factor de actividad (Mifflin o Katch × 1,55–1,725) pueden sobreestimar si parte del entrenamiento es de baja intensidad. Las fórmulas MET del Compendio sí sirven, corregidas por su basal.
- **El dato que manda es la tendencia del peso:** gasto real = ingesta + kg bajados × **7.700 kcal/kg** ÷ días, en ventanas de 2 semanas o más.
  - 7.700 kcal es 1 kg de tejido adiposo (~85 % grasa).
  - En las primeras semanas el peso baja más rápido de lo que da el déficit (agua y glucógeno), así que con menos de 2 semanas el resultado es preliminar.
- **Recalibración:** con la tendencia del peso, en las fechas del plan. Cada vez se agrega un «Resultado N» al análisis y se actualiza el factor de WHOOP.

## Fuentes de datos
- **Se acepta cualquier dispositivo** cuyos datos se puedan exportar y convertir a los CSV de `formatos.md`, con las mismas reglas que los soportados. Lo que importa es la tendencia de una misma fuente, no su marca.
- **Cada dispositivo tiene su propio sesgo:** su factor de gasto parte en 1,0 y se calibra con la tendencia del peso. Nunca se copia el factor de otro dispositivo ni de otra persona.
- **Umbrales propios:** la HRV, la FC en reposo y el sueño se miden distinto en cada dispositivo. Los umbrales salen del promedio de la persona con ese dispositivo.
- **Si falta un dato, su regla no se aplica** (ej.: sin recovery, la regla de recuperación usa solo HRV, FC en reposo y sueño) y queda anotado en el plan. Sin pesa con composición, alcanzan el peso, la cintura y la fuerza.
- **No se mezclan dispositivos:** si cambia, se anota la fecha y se recalibra desde ahí.

## Lecciones aprendidas
Salieron del historial de versiones de un plan real y sirven para cualquier persona.
- **Semana 0 de adaptación:** la primera semana baja sobre todo agua y glucógeno. Se usa para ajustar el menú y fijar la línea base (promedio de 7 días); el día 1 parte el lunes siguiente.
- **Sin recorte en los días sin entrenamiento:** bajar calorías ese día dejó déficits grandes que terminaron en atracones. Mejor menú completo y una caminata.
- **Snack de emergencia en 2 pasos:** primero algo chico (~50 kcal) y, solo si sigue el hambre, uno con proteína (~150–200 kcal). Se anota y no cuenta como salirse del plan; casi siempre basta el primero.
- **Un solo menú por tipo de día:** un menú distinto para cada día complica cumplirlo. Lo que cambia según el horario es la hora de las comidas, no los alimentos.
- **Comidas antes del entrenamiento que no haya que cocinar** (pan, fruta, batido): lo que exige cocinar temprano no se cumple.
- **La adherencia antes que el recorte:** cuando el ritmo queda bajo, primero mirar cuántos días se cumplió el menú. Las salidas del fin de semana suelen explicar la diferencia; recortar calorías no la arregla.
- **Control del balance:** el déficit acumulado (gasto corregido − ingesta) debe calzar con la tendencia del peso × 7.700 kcal/kg. La masa grasa de la pesa no sirve para este control: en unas semanas su ruido es mayor que el cambio.
- **Músculo:** la masa libre de grasa de la bioimpedancia se mueve casi igual que el agua. El músculo se sigue con la fuerza (máximos o repeticiones con la misma carga) y con meses de tendencia, no con la pesa.
- **Lo que se come de madrugada, antes de dormir, cuenta en el día anterior.**
- **Las decisiones de la persona se respetan y se registran:** si decide aplicar solo una parte de una regla, se anota con la fecha y se reevalúa en la revisión siguiente.
