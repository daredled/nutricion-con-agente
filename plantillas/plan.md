# Plan fase 1: déficit (semana 0 desde el AAAA-MM-DD; día 1: AAAA-MM-DD)

Objetivo: **meta de % de grasa** (y la que corresponda: grasa visceral, cintura), según la pesa.
Base del cálculo: `perfil.md`, pesaje del día 0 y N días de datos del dispositivo (`registros/…`).

<!--
Copiar a persona/plan/AAAA-MM-DD_plan-fase1.md y llenarlo siguiendo crear-plan.md.
visualizacion/generar.py lee tres cosas de este archivo, así que su formato no se puede cambiar:
  1. Las versiones del encabezado: «**vN (AAAA-MM-DD):**» o «**vN.M (…):**». El panel muestra la más alta.
  2. La tabla «Pesos de referencia»: filas «| AAAA-MM-DD | semana | ~NN,N kg | nota |».
  3. La tabla «Hitos»: filas «| AAAA-MM-DD | N días | ~NN,N kg | NN,N kg | … |».
Los decimales pueden ir con coma o con punto.
-->

> **v1 (AAAA-MM-DD):** plan inicial.

---

## 1. Cálculos

### Gasto energético
| | kcal/día |
|---|---|
| Dispositivo, promedio de N días (sin corregir) | |
| Fórmula de referencia (Mifflin o Katch × factor de actividad) | |
| **Gasto de trabajo** | **~N** (rango N–N) |

- De dónde sale el gasto de trabajo y qué supuestos tiene (sesiones por semana, pasos).
- Se recalibra con la tendencia del peso a las 2 semanas (`analisis/gasto-calorico.md`).

### Déficit y macros
| | Meta diaria |
|---|---|
| **Calorías** | **~N kcal**, un déficit de ~N kcal (−20 a −25 %) |
| **Pasos** | **N o más al día** |
| **Proteína** | **~N g** (1,6–2,2 g/kg de peso, o 2,3–3,1 g/kg de masa libre de grasa) |
| **Grasa** | **~N g** (20–30 % de las kcal) |
| **Carbohidratos** | **~N g**, el resto, alrededor del entrenamiento |
| Fibra | ≥25–30 g |
| Sodio | Límite general o el de su médico |

### Ritmo y fecha estimada
- **Línea base:** promedio de los 7 pesajes de la semana 0: **NN,N kg**, con su % de grasa y masa libre de grasa promedio.
- **Peso objetivo:** rango, calculado como masa libre de grasa ÷ (1 − meta de grasa), con y sin perder 10–20 % de lo bajado como masa libre de grasa. **El criterio real es el % de grasa y la cintura, no el peso.**
- **Ritmo esperado:** déficit × 7 ÷ 7.700 kg por semana (0,5–1 % del peso por semana como máximo).

#### Pesos de referencia (escenario central: N kg/semana desde el día 1, promedio de 7 días)
| Fecha | Semana | Peso esperado | Nota |
|---|---|---|---|
| AAAA-MM-DD | 0 | NN,N kg | Día 1. Línea base: promedio de 7 días de la semana 0 |
| AAAA-MM-DD | 1 | ~NN,N kg | |
| AAAA-MM-DD | 2 | ~NN,N kg | Recalibración del gasto y primera evaluación de las reglas |
| AAAA-MM-DD | N | ~NN,N kg | **Zona meta** |

- Si el promedio de 7 días queda **más de 1 kg por encima** de esta tabla durante 2 semanas, se aplican las reglas de la sección 4.

#### Hitos a 7, 15, 30, 60 y 90 días
Se miden con el **promedio de 7 días**, nunca con un pesaje suelto.

| Fecha | Hito | Peso esperado | Va bien si queda bajo | Grasa esperada | Qué representa |
|---|---|---|---|---|---|
| AAAA-MM-DD | 7 días | ~NN,N kg | NN,N kg | ~N % | |
| AAAA-MM-DD | 15 días | ~NN,N kg | NN,N kg | ~N % | Primera evaluación de las reglas |
| AAAA-MM-DD | 30 días | ~NN,N kg | NN,N kg | ~N % | |
| AAAA-MM-DD | 60 días | ~NN,N kg | NN,N kg | ~N % | |
| AAAA-MM-DD | 90 días | ~NN,N kg | NN,N kg | ~N % | |

En todos los hitos, además: masa libre de grasa ≥ N kg (línea base menos ~1 kg), cintura (~1 cm menos por kg bajado), menú cumplido ≥90 % y pasos en 5 de 7 días.

---

## 2. Menús
Gramos exactos, diciendo si son en crudo o en cocido, con kcal y macros por comida, y la sal agregada en gramos.

### Menú A: días con entrenamiento
| Hora | Comida | Alimentos | kcal | P | C | G |
|---|---|---|---|---|---|---|
| | **Desayuno** | | | | | |
| | **Total** | | **~N** | | | |

### Excepciones
- **Día sin entrenamiento:** menú completo + caminata (sin recorte; ver `metodologia.md`).
- **Doble turno o sesión muy intensa:** qué se agrega y cuánto.
- **Snack de emergencia:** primero uno chico y, solo si sigue el hambre, uno con proteína. Se anota y no cuenta como salirse del plan.

### Intercambios
Equivalencias por gramo dentro de cada grupo (proteína, carbohidrato, grasa).

### Suplementos
Los que toma, con dosis y cuándo.

---

## 3. Salud
Las reglas médicas del perfil aplicadas al menú: sodio por comida, potasio, cafeína, hidratación, cuándo derivar al médico.

---

## 4. Seguimiento y reglas de ajuste

### Qué mandar
| Frecuencia | Qué | Cómo |
|---|---|---|
| **Diario** | Pesaje | En ayunas, después de ir al baño, siempre a la misma hora |
| Diario | Dispositivo (sueño, gasto, pasos) | Lo descarga el agente |
| **Lunes** | **Cintura** | Con huincha a la altura del ombligo, en ayunas |
| Cada 2 semanas | Prueba de fuerza | Un mismo ejercicio de referencia |

### Reglas (cada lunes, con el promedio de 7 días)
Rango objetivo: **N a N kg por semana**, cumpliendo el menú al menos 90 %.

| Situación | Ajuste |
|---|---|
| Baja **menos que el mínimo del rango** durante 2 semanas | Primero revisar el cumplimiento del menú; si se cumplió, +pasos y −150 kcal |
| Baja dentro del rango | Sin cambios |
| Baja **más que el máximo del rango** durante 2 semanas | +150 kcal de carbohidratos |
| Masa libre de grasa cae **más de 1,5 kg en 4 semanas** y además baja la fuerza | +150 kcal y revisar la proteína |
| HRV del promedio de 7 días bajo su referencia − 1 DE, o recovery baja varios días | Priorizar el sueño; si se repite, +150 kcal alrededor del entrenamiento |
| El peso baja pero la cintura no, en 3 semanas | Revisar retención de líquido antes de cambiar calorías |
| Hambre alta persistente | Más verduras y otro reparto, mismas calorías |

- **Límite inferior:** no bajar de N kcal sin revisar todo el plan.
- **Pausa programada:** entre las semanas 8 y 10 se evalúa 1 semana en mantención.
- **Nunca se ajusta por el dato de un solo día.**

---

## 5. Transición a la fase 2
- **Criterio:** meta de grasa sostenida 2 semanas, con la cintura en descenso.
- **Paso 1:** mantención 2 a 4 semanas.
- **Paso 2:** superávit de +200 a 300 kcal, proteína ~1,8–2 g/kg, máximo 0,25 kg por semana.

---

## Lista de compras semanal
| Alimento | Cantidad |
|---|---|
