# Gasto calórico: dispositivo contra fórmulas y balance de energía

Objetivo: estimar el gasto diario real de NOMBRE y cuánto se equivoca su dispositivo, para calibrar el déficit del plan.
Copiar a `persona/analisis/gasto-calorico.md`. Cada recalibración agrega un «Resultado N» al final. **Vigente: (ninguno todavía), factor × 1,0.**

---

## Metodología

Se usan tres métodos independientes y se comparan. Manda el balance de energía.

### 1. Balance de energía (método de referencia)
- Gasto real = ingesta media + (kg bajados × 7.700 kcal) ÷ días.
- **Ingesta:** `ingesta.menu` de `config.toml` por día, más las excepciones (doble turno) y lo anotado en `registros/ingesta.csv`.
- **Cambio de peso:** pendiente de una regresión lineal de los pesajes diarios, o diferencia entre promedios de 7 días. Nunca un pesaje suelto.
  - Al comparar promedios de 7 días, el período del déficit va del centro de la primera ventana al centro de la segunda, no del primer al último día.
- **Agua y glucógeno:** en la primera semana de un déficit, y después de cambios de sal o de carbohidratos, gran parte de la baja es agua. Por eso:
  - Con menos de 2 semanas el resultado es preliminar; se dan escenarios (0,2 / 0,4 / 0,6 kg de grasa).
  - Con 2 semanas o más ya no hace falta separar el agua, salvo cambios bruscos de sal o de carbohidratos.
- La masa grasa de la pesa no sirve para esto: su ruido es mayor que el cambio de unas semanas.

### 2. Fórmulas por deporte (METs del Compendio de Actividad Física, Ainsworth 2011/2024)
- Gasto del día = **basal × 1,2** (base sedentaria) + **gasto neto de cada sesión**.
- Gasto neto de una sesión = (MET − 1) × peso (kg) × horas.
- Basal: Katch-McArdle = 370 + 21,6 × masa libre de grasa, o Mifflin-St Jeor.
- **Corrección por basal:** el MET supone 1 kcal/kg/h. Con más peso el basal por kilo baja: se multiplica el gasto neto por basal ÷ 24 ÷ peso.

| Actividad | MET (rango) | Código del Compendio de referencia |
|---|---|---|
| | | |

### 3. Dispositivo
- Gasto del día y de cada entrenamiento desde `registros/`.
- WHOOP: su «día» es un ciclo de dormirse a dormirse (19 a 29 h). Se compara llevado a 24 h (`day_kcal` ÷ horas del ciclo × 24; las horas están en `registros/whoop_ciclos.csv`).

---

## Cómo repetirlo (para cada recalibración)
1. Tomar una ventana de al menos 14 días desde el día 1, sin cambios de sal o de carbohidratos al inicio.
2. Ingesta: `ingesta.menu` de `config.toml` + excepciones + `registros/ingesta.csv`.
3. Peso: pendiente de la regresión de los pesajes, o diferencia entre promedios de 7 días bien alineada (ver arriba).
4. Gasto real = ingesta media + (kg bajados × 7.700) ÷ días.
5. Comparar con el promedio del dispositivo en la misma ventana (solo días completos, llevado a 24 h) y con el cálculo MET corregido.
6. Agregar un «Resultado N» con la fecha, los datos, la comparación, las conclusiones y las limitaciones. Actualizar `whoopFactor` y `whoopFactorRange` en `config.toml`.
7. **Ojo con la circularidad:** desde que el factor se calibra con la tendencia del peso, que el déficit corregido calce con el peso es un control de las cuentas, no una prueba independiente.

## Evidencia (consultada el 2026-10-04)
- No hay validaciones independientes revisadas por pares de las calorías de WHOOP.
- Murakami et al. 2019, JMIR mHealth (12 dispositivos contra agua doblemente marcada): 10 de 12 subestimaron el gasto por actividad. https://pubmed.ncbi.nlm.nih.gov/31376273/
- Fuller et al. 2020, JMIR mHealth (revisión sistemática): menos del 10 % de las estimaciones de gasto dentro de ±3 %; 54 % subestimaron. https://pmc.ncbi.nlm.nih.gov/articles/PMC7509623/
- O'Driscoll et al. 2020, BJSM (metaanálisis de 60 estudios): precisión muy variable según la actividad. https://pubmed.ncbi.nlm.nih.gov/30194221/
- WHOOP reconoce que la frecuencia cardíaca capta poco la carga del trabajo de fuerza (Strength Trainer, 2023).

---

## Resultado 1: … (AAAA-MM-DD a AAAA-MM-DD), calculado el AAAA-MM-DD
### Datos
### Comparación
| Método | Gasto diario | Contra el balance |
|---|---|---|
### Conclusiones
### Limitaciones
