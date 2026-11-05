# Gasto calórico: Garmin contra fórmulas y balance de energía

Persona ficticia: datos inventados. El método está en `plantillas/gasto-calorico.md`.
**Vigente: Resultado 1 (2026-11-02), factor de Garmin × 1,13.** Próxima revisión: 2026-11-30.

---

## Resultado 1: 14 días (2026-10-19 a 2026-11-01), calculado el 2026-11-02

### Datos
- Pesajes del 2026-10-19 al 2026-11-02 (15): pendiente de la regresión **−0,089 kg/día (−1,24 kg en 14 días)**. La semana 0 queda fuera (agua y glucógeno).
- Ingesta: menú 1.690 × 12 días + 2.590 (cena fuera, 24-10) + 2.340 (cumpleaños, 31-10) = **~1.800 kcal/día**.
- Garmin: **2.194 kcal/día** (días completos; Garmin da días calendario, así que el gasto ya es de 24 h).

### Comparación
| Método | Gasto diario | Contra el balance (~2.485) |
|---|---|---|
| Garmin | ~2.194 | −291 (−12 %) |
| Mifflin × 1,55 | ~2.230 | −255 |
| **Balance de energía** | **~2.485** (1.800 + 1,24 × 7.700 ÷ 14) | referencia |

### Conclusiones
1. **Factor de Garmin: × 1,13** (rango 1,05–1,20). Actualizado en `config.toml`.
2. El déficit real con el menú es de ~800 kcal/día los días que se cumple (~32 %), sobre el 20–25 % del plan. Como el ritmo (0,62 kg/semana) está dentro del rango y no hay hambre alta, no se cambian las calorías; se vigila el hambre y la HRV.

### Limitaciones
- 2 semanas: ±0,3 kg en el peso mueven el resultado ±165 kcal/día.
- Las comidas fuera del plan son estimaciones.
