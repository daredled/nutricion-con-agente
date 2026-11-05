"""Convierte la exportación diaria de Garmin (entrada/garmin-*.csv) al formato estándar (registros/actividad.csv).

Uso: uv run ejemplo/importar/garmin.py          (o persona/importar/garmin.py)

Es el modelo de un conversor: lee las exportaciones tal como salen del dispositivo, sin tocarlas, y escribe las
columnas de formatos.md. Las fechas que ya estaban en actividad.csv se reemplazan con lo más nuevo; las demás se
conservan. El formato de esta exportación es inventado (persona ficticia): con un archivo real, ajustar COLUMNS.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "registros" / "actividad.csv"
FIELDS = ["date", "recovery", "hrv_ms", "resting_hr", "sleep_h", "day_strain", "day_kcal", "steps", "workouts",
          "cycle_complete"]
# Columna de la exportación -> columna estándar.
COLUMNS = {"Date": "date", "Steps": "steps", "Total Calories": "day_kcal", "Resting Heart Rate": "resting_hr",
           "HRV Overnight Avg (ms)": "hrv_ms"}


def sleep_hours(text: str) -> str:
    """'7:33' -> '7.55'."""
    if not text:
        return ""
    h, m = text.split(":")
    return f"{int(h) + int(m) / 60:.2f}"


def workouts(text: str) -> str:
    """'Strength Training|60|230; Running|45|390' -> 'strength_training 60min 230kcal | running 45min 390kcal'."""
    out = []
    for part in filter(None, (p.strip() for p in text.split(";"))):
        kind, minutes, kcal = part.split("|")
        out.append(f"{kind.strip().lower().replace(' ', '_')} {minutes}min {kcal}kcal")
    return " | ".join(out)


def main() -> None:
    rows = {}
    if OUT.exists():
        with OUT.open(newline="") as f:
            rows = {r["date"]: r for r in csv.DictReader(f)}
    for path in sorted((HERE / "entrada").glob("garmin-*.csv")):  # el último archivo manda
        with path.open(newline="") as f:
            for r in csv.DictReader(f):
                row = {std: r.get(col, "") for col, std in COLUMNS.items()}
                row["sleep_h"] = sleep_hours(r.get("Sleep Time", ""))
                row["workouts"] = workouts(r.get("Activities", ""))
                row["cycle_complete"] = "yes" if row["date"] < date.today().isoformat() else "no"
                rows[row["date"]] = row
    with OUT.open("w", newline="") as f:
        out = csv.DictWriter(f, FIELDS, extrasaction="ignore")
        out.writeheader()
        out.writerows(rows[d] for d in sorted(rows))
    print(f"{len(rows)} días en {OUT.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
