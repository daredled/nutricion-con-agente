# Operación con Ana (persona ficticia)

Lo propio de Ana al operar. Lo general está en `AGENTS.md`. Idioma: español neutro.

## Plan y archivos
- **Plan vigente:** `plan/2026-10-18_plan-fase1.md` (v1.1).
- **`analisis/gasto-calorico.md`:** recalibrado el 2026-11-02 (Resultado 1); el próximo, el 2026-11-30.

## Decisiones del usuario (con fecha)
- **Presión:** no tiene tensiómetro; no se pide.
- **Pasos:** meta ≥8.000 desde el día 1.

## Revisiones clave
- La semana 0 (adaptación) fue del 2026-10-12 al 2026-10-18 y el **día 1 es el 2026-10-19** (lunes).
- **2026-11-02:** recalibración del gasto (Resultado 1) e hito de 15 días.
- **2026-11-30:** segunda recalibración; evaluar la pausa en mantención entre las semanas 8 y 10.
- Hitos de 7, 15, 30, 60 y 90 días: 2026-10-25, 2026-11-02, 2026-11-17, 2026-12-17 y 2027-01-16.

## Técnico de este equipo
- Dispositivos: reloj Garmin y pesa Fitdays (cuenta con un solo perfil, sin `suid`). Sin tensiómetro.
- **Garmin:** exporta un CSV diario a `entrada/garmin-AAAA-MM-DD.csv`; se convierte con `uv run ejemplo/importar/garmin.py` a `registros/actividad.csv` (desde el 2026-10-12).
