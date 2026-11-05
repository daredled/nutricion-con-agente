"""Genera persona/panel.html: el panel de seguimiento con WHOOP, Fitdays y la presión.

Uso: uv run visualizacion/generar.py [carpeta]

La carpeta de la persona es `persona/` por defecto (ej.: `uv run visualizacion/generar.py ejemplo`).
Lee config.toml, los CSV de persona/registros/, la tabla de pesos de referencia del
plan y los pesos de seguimiento.md que no estén en Fitdays (por ejemplo el día 0, borrado en
la nube), y los incrusta como JSON en la plantilla.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import tomllib
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONA = ROOT / (sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else "persona")
REG = PERSONA / "registros"
TEMPLATE = Path(__file__).with_name("panel.template.html")
OUT = PERSONA / "panel.html"
CONFIG = tomllib.loads((PERSONA / "config.toml").read_text())
PLAN = PERSONA / CONFIG["plan"]

DATA_START = CONFIG["fechas"]["datos_desde"]
DAY0 = CONFIG["fechas"]["dia_0"]
SEG_BASE = CONFIG["fechas"]["base_segmentos"]
PLAN_START = CONFIG["fechas"]["dia_1"]
FITDAYS_SUID = CONFIG.get("fitdays", {}).get("suid", "")
INTAKE = CONFIG["ingesta"]["menu"]
# Excepciones opcionales del menú. Sin ellas: sin variante sin entreno, y doble turno cualquier día.
REST_CUT = CONFIG["ingesta"].get("sin_entreno_kcal", 0)
REST_FIRST_ONLY_FROM = CONFIG["ingesta"].get("sin_entreno_solo_primero_desde", "")
REST_CUT_UNTIL = CONFIG["ingesta"].get("sin_entreno_hasta", "")
DOUBLE_WEEKEND_FROM = CONFIG["ingesta"].get("doble_turno_finde_desde", "9999-12-31")
PLAN_RULES = CONFIG["reglas"]
WORKOUTS = CONFIG.get("entrenamientos", [])
for w in WORKOUTS:  # `tipo` es el nombre del entrenamiento en el CSV; `whoop` es el nombre antiguo de la clave
    w.setdefault("tipo", w.get("whoop", ""))
WORKOUT_TYPES = {w["tipo"]: w["nombre"] for w in WORKOUTS}
# De dónde sale cada dato (formatos.md). Sin [fuentes]: Fitdays, WHOOP y Withings.
SOURCES = {"pesa": "fitdays", "actividad": "whoop", "presion": "withings", **CONFIG.get("fuentes", {})}
DEVICE = SOURCES.get("dispositivo") or ("WHOOP" if SOURCES["actividad"] == "whoop" else "el dispositivo")
WEIGH_CSV = REG / ("fitdays.csv" if SOURCES["pesa"] == "fitdays" else "pesa.csv")
ACTIVITY_CSV = REG / ("whoop_diario.csv" if SOURCES["actividad"] == "whoop" else "actividad.csv")
NO_SESSION = [w["nombre"] for w in WORKOUTS if not w.get("sesion", True)]
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
SEGMENTS = [
    ("Brazo izq.", "left_arm"), ("Brazo der.", "right_arm"), ("Tronco", "trunk"),
    ("Pierna izq.", "left_leg"), ("Pierna der.", "right_leg"),
]


def num(v: str | None) -> float | None:
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def plan_reference() -> list[list]:
    """Tabla 'Pesos de referencia' del plan: | AAAA-MM-DD | 1 | ~80,0 kg | ..."""
    ref = []
    for line in PLAN.read_text().splitlines():
        m = re.match(r"^\| (\d{4}-\d{2}-\d{2}) \| \d+ \| \**~?([\d.,]+) kg", line)
        if m:
            ref.append([m.group(1), float(m.group(2).replace(",", "."))])
    return ref


def plan_version() -> str:
    """La versión más alta anotada en el encabezado del plan («**v5.3 (…»)."""
    found = re.findall(r"\*\*v(\d+(?:\.\d+)?) \(", PLAN.read_text())
    return "v" + max(found, key=lambda v: tuple(map(int, v.split(".")))) if found else ""


def plan_milestones() -> list[list]:
    """Tabla 'Hitos' del plan: | AAAA-MM-DD | 15 días | ~79,0 kg | 80,0 kg | ..."""
    out = []
    for line in PLAN.read_text().splitlines():
        m = re.match(r"^\| (\d{4}-\d{2}-\d{2}) \| (\d+ días) \| ~?([\d.,]+) kg \| ([\d.,]+) kg", line)
        if m:
            out.append([m.group(1), m.group(2), float(m.group(3).replace(",", ".")), float(m.group(4).replace(",", "."))])
    return out


def goal_date(ref: list[list]) -> str:
    return ref[-1][0] if ref else PLAN_START


def weigh_ins() -> list[dict]:
    """Un pesaje por día (el primero, de la mañana). Completa con seguimiento.md los días sin Fitdays."""
    by_day: dict[str, dict] = {}
    seg_pct = segment_pcts()
    for r in read_csv(WEIGH_CSV):
        if FITDAYS_SUID and r.get("suid") and r["suid"] != FITDAYS_SUID:
            continue
        r.setdefault("time", "")
        if r["date"] in by_day and by_day[r["date"]]["t"] <= r["time"]:
            continue
        pcts = seg_pct.get(r.get("data_id"))
        if pcts is None and r.get("data_id", "").startswith("manual-"):
            # Fila manual: los % del estándar están en el registro del día, copiados de la captura.
            pcts = {k: v[2:] for k, v in (segments_md(REG / f"{r['date']}.md") or {}).items()}
        by_day[r["date"]] = {
            "d": r["date"], "t": r["time"][:5], "w": num(r.get("weight_kg")),
            "fatPct": num(r.get("body_fat_pct")), "fatKg": num(r.get("fat_mass_kg")),
            "ffmKg": num(r.get("fat_free_mass_kg")), "visceral": num(r.get("visceral_fat")),
            "muscleKg": num(r.get("muscle_kg")), "skmKg": num(r.get("skeletal_muscle_kg")), "src": "fitdays",
            "seg": {key: [num(r.get(f"fat_{key}_kg")), num(r.get(f"muscle_{key}_kg")),
                         *(pcts or {}).get(key, [None, None])] for _, key in SEGMENTS},
        }
    seguimiento = REG / "seguimiento.md"
    for line in seguimiento.read_text().splitlines() if seguimiento.exists() else []:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or not re.match(r"\d{4}-\d{2}-\d{2}$", cells[0]) or cells[0] in by_day:
            continue
        w = num(cells[1])
        if w is None:
            continue
        by_day[cells[0]] = {
            "d": cells[0], "t": "", "w": w, "fatPct": num(cells[3]), "fatKg": num(cells[4]),
            "ffmKg": num(cells[5]), "visceral": num(cells[6]), "muscleKg": None, "skmKg": None, "src": "registro",
            "seg": None,
        }
    fill_gaps(by_day)
    return [by_day[d] for d in sorted(by_day)]


def fill_gaps(by_day: dict[str, dict]) -> None:
    """Día suelto sin pesaje entre dos pesajes: promedio de ambos, marcado como «estimado».

    Solo sirve para que los gráficos se vean completos: no entra en los promedios de 7 días (ver build).
    """
    for d in sorted(by_day):
        nxt = (date.fromisoformat(d) + timedelta(days=2)).isoformat()
        mid = (date.fromisoformat(d) + timedelta(days=1)).isoformat()
        if d < DATA_START or mid in by_day or nxt not in by_day:
            continue
        a, b = by_day[d], by_day[nxt]
        avg = lambda x, y: round((x + y) / 2, 2) if x is not None and y is not None else None
        seg = None
        if a["seg"] and b["seg"]:
            seg = {k: [avg(x, y) for x, y in zip(a["seg"][k], b["seg"][k])] for k in a["seg"]}
        by_day[mid] = {"d": mid, "t": "", "src": "estimado", "seg": seg,
                       **{k: avg(a[k], b[k]) for k in ("w", "fatPct", "fatKg", "ffmKg", "visceral", "muscleKg", "skmKg")}}


def segment_pcts() -> dict[str, dict[str, list]]:
    """% del estándar por segmento (grasa, músculo) desde la respuesta cruda de Fitdays, por data_id del pesaje.

    El CSV de fitdays-sync no los exporta; son los porcentajes de la figura del reporte ('Segmental fat
    analysis' y 'Muscle balance').
    """
    path = PERSONA / "fitdays" / "raw" / "sync.json"
    if SOURCES["pesa"] != "fitdays" or not path.exists():
        return {}
    raw = json.loads(path.read_text())
    imp = {i["data_id"]: i for i in raw.get("impedance_list", [])}
    keys = {"left_arm": "lh", "right_arm": "rh", "trunk": "torso", "left_leg": "lf", "right_leg": "rf"}
    out = {}
    for w in raw.get("weight_list", []):
        i = imp.get(w.get("imp_data_id"))
        if i:
            out[w["data_id"]] = {k: [round(i[f"{p}_bfr"], 1), round(i[f"{p}_rom"], 1)] for k, p in keys.items()}
    return out


def parse_workouts(text: str) -> list[list]:
    """'basketball 85min 323kcal strain 7.0 | walking 22min 31kcal strain 0.0' -> [[tipo, min, kcal], ...]."""
    out = []
    for part in text.split("|"):
        m = re.match(r"\s*(\S+) (\d+)min (\d+)kcal", part)
        if m:
            out.append([WORKOUT_TYPES.get(m.group(1), "Otro"), int(m.group(2)), int(m.group(3))])
    return out


def rolling(points: dict[str, float], days: int = 7, min_n: int = 5, at: list[str] | None = None) -> dict[str, float]:
    """Promedio de los valores de los últimos `days` días calendario, si hay al menos `min_n`.

    Se calcula en cada fecha de `at` (por defecto, las de `points`).
    """
    out = {}
    for d in at or points:
        end = date.fromisoformat(d)
        vals = [points[(end - timedelta(days=i)).isoformat()] for i in range(days)
                if (end - timedelta(days=i)).isoformat() in points]
        if len(vals) >= min_n:
            out[d] = round(sum(vals) / len(vals), 2)
    return out


def weekly_history(weighs: list[dict]) -> list[dict]:
    """Historial de los lunes (día de la revisión semanal): promedio de los 7 días que terminan ese lunes.

    Peso, masa muscular, músculo esquelético, masa grasa y % de grasa, como el historial de InBody. `n` = pesajes de la ventana (sin estimados).
    El lunes que viene entra con la semana en curso (`open`: promedio incompleto, con los pesajes que van).
    """
    real = [w for w in weighs if w["src"] != "estimado"]
    out = []
    d = date.fromisoformat(DATA_START)
    while d - timedelta(days=6) <= date.today():
        at = [d.isoformat()]
        row = {"d": d.isoformat(), "n": sum(d - timedelta(days=6) <= date.fromisoformat(w["d"]) <= d for w in real),
               "open": d > date.today()}
        for key in ("w", "muscleKg", "skmKg", "fatKg", "fatPct"):
            row[key] = rolling({w["d"]: w[key] for w in real if w[key] is not None}, min_n=1, at=at).get(at[0])
        if row["n"]:
            out.append(row)
        d += timedelta(days=7)
    return out


def cycle_hours() -> dict[str, float]:
    """Horas de cada ciclo completo de WHOOP, por día (el mismo día que le asigna whoop-sync: inicio local + 12 h).

    `day_kcal` es de un ciclo (de dormirse a dormirse: 19 a 29 h), no de 24 h. cycles.json solo trae la última
    ventana del sync, así que registros/whoop_ciclos.csv guarda el historial.
    """
    if SOURCES["actividad"] != "whoop":
        return {}  # Otros dispositivos: una fila por día calendario, el gasto ya es de 24 h.
    path = REG / "whoop_ciclos.csv"
    hours = {r["date"]: float(r["cycle_h"]) for r in read_csv(path)}
    raw = PERSONA / "whoop" / "raw" / "cycles.json"
    for c in json.loads(raw.read_text()) if raw.exists() else []:
        if c.get("end"):
            start = datetime.fromisoformat(c["start"])
            sign, hh, mm = c["timezone_offset"][0], c["timezone_offset"][1:3], c["timezone_offset"][4:6]
            offset = timedelta(hours=int(hh), minutes=int(mm)) * (-1 if sign == "-" else 1)
            d = (start + offset + timedelta(hours=12)).date().isoformat()
            hours[d] = round((datetime.fromisoformat(c["end"]) - start).total_seconds() / 3600, 2)
    with path.open("w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["date", "cycle_h"])
        out.writerows(sorted(hours.items()))
    return hours


def segments_md(path: Path) -> dict | None:
    """Tabla '## Segmentos' de un registro diario: | Brazo izq. | 1.9 | 4.3 | (+ % del estándar, si están)."""
    if not path.exists():
        return None
    names = dict(SEGMENTS)
    seg = {}
    for line in path.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) in (3, 5) and cells[0] in names:
            seg[names[cells[0]]] = [num(c) for c in cells[1:]] + [None] * (5 - len(cells))
    return seg or None


def intake_days(whoop: list[dict]) -> dict[str, dict]:
    """Ingesta estimada por día: menú, menos la variante sin entreno, más el doble turno; registros/ingesta.csv manda.

    Un día sin entreno es un día completo de WHOOP sin sesiones (las caminatas no cuentan); el doble turno, 2 o más
    (desde DOUBLE_WEEKEND_FROM, solo sábado y domingo).
    """
    def menu(d: str) -> int | None:
        v = None
        for start, k in INTAKE:
            if d >= start:
                v = k
        return v

    out, prev_rest = {}, False
    for w in sorted(whoop, key=lambda w: w["d"]):
        sessions = [t for t, _, _ in w["wo"] if t not in NO_SESSION]
        rest = w["complete"] and not sessions
        base = menu(w["d"])
        if base is not None and w["complete"]:
            weekend = date.fromisoformat(w["d"]).weekday() >= 5
            if PLAN_RULES.get("doubleExtra") and len(sessions) >= 2 and (weekend or w["d"] < DOUBLE_WEEKEND_FROM):
                out[w["d"]] = {"kcal": base + PLAN_RULES.get("doubleExtra", 0), "src": "doble turno"}
            elif rest and PLAN_START <= w["d"] <= REST_CUT_UNTIL and not (w["d"] >= REST_FIRST_ONLY_FROM and prev_rest):
                out[w["d"]] = {"kcal": base - REST_CUT, "src": "sin entreno"}
            else:
                out[w["d"]] = {"kcal": base, "src": "menú"}
        prev_rest = rest
    for r in read_csv(REG / "ingesta.csv"):
        if num(r["kcal"]) is not None:
            out[r["date"]] = {"kcal": num(r["kcal"]), "src": r.get("nota") or "estimada"}
    return out


def build() -> dict:
    ref = plan_reference()
    weighs = weigh_ins()
    # Los días estimados (fill_gaps) no cuentan en los promedios, pero sí reciben el de su fecha.
    points = {w["d"]: w["w"] for w in weighs if w["w"] and w["src"] != "estimado"}
    at = [w["d"] for w in weighs if w["w"]]
    avg7 = rolling(points, at=at)
    # Promedio parcial (2 a 4 pesajes en la ventana): el panel lo dibuja punteado antes de que exista el de 7 días.
    partial = rolling(points, min_n=2, at=at)
    counts = {d: sum((date.fromisoformat(d) - timedelta(days=i)).isoformat() in points for i in range(7)) for d in at}
    for w in weighs:
        w["avg7"] = avg7.get(w["d"])
        w["avg7p"] = partial.get(w["d"]) if w["avg7"] is None else None
        w["avg7n"] = counts.get(w["d"])

    whoop, cycles = [], cycle_hours()
    for r in read_csv(ACTIVITY_CSV):
        kcal, cycle_h = num(r.get("day_kcal")), cycles.get(r["date"])
        whoop.append({
            "d": r["date"], "rec": num(r.get("recovery")), "hrv": num(r.get("hrv_ms")),
            "rhr": num(r.get("resting_hr")), "sleep": num(r.get("sleep_h")),
            # Gasto llevado a 24 h (analisis/gasto-calorico.md, Resultado 3); kcalRaw es lo que marcó WHOOP en el ciclo.
            "kcal": round(kcal / cycle_h * 24) if kcal and cycle_h else kcal, "kcalRaw": kcal, "cycleH": cycle_h,
            "strain": num(r.get("day_strain")), "complete": r.get("cycle_complete") == "yes",
            "steps": num(r.get("steps")), "workouts": r.get("workouts") or "",
            "wo": parse_workouts(r.get("workouts") or ""),
        })
    hrv7 = rolling({w["d"]: w["hrv"] for w in whoop if w["hrv"]})
    for w in whoop:
        w["hrv7"] = hrv7.get(w["d"])

    bp = [{"d": r["date"], "t": r.get("time", ""), "sys": num(r.get("systolic")), "dia": num(r.get("diastolic")),
           "pulse": num(r.get("pulse"))} for r in read_csv(REG / "presion.csv")]

    history = weekly_history(weighs)
    # The panel shows day 0 onward; earlier rows only feed the 7-day averages above.
    weighs = [w for w in weighs if w["d"] >= DATA_START]
    whoop = [w for w in whoop if w["d"] >= DATA_START]
    bp = [b for b in bp if b["d"] >= DATA_START]

    # Una pesa sin segmentos deja las filas con valores vacíos: cuentan como sin segmentos.
    has_seg = lambda seg: bool(seg) and any(v is not None for vals in seg.values() for v in vals)
    seg0 = next((w for w in weighs if w["d"] == SEG_BASE and has_seg(w["seg"])), None)
    base_seg = seg0["seg"] if seg0 else segments_md(REG / f"{SEG_BASE}.md")
    last = next((w for w in reversed(weighs) if has_seg(w["seg"])), None)
    return {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "today": date.today().isoformat(),
        "planStart": PLAN_START, "day0": DAY0, "dataStart": DATA_START,
        "plan": {**PLAN_RULES, "version": plan_version(), "ref": ref, "goalDate": goal_date(ref), "intake": INTAKE, "intakeDays": intake_days(whoop), "milestones": plan_milestones(), "workouts": WORKOUTS, "noSession": NO_SESSION, "device": DEVICE,
                 "bpSource": SOURCES["presion"] != "ninguna"},
        "weigh": weighs,
        "history": history,
        "whoop": whoop,
        "bp": bp,
        "segments": {
            "base": {"d": SEG_BASE, "seg": base_seg} if base_seg else None,
            "last": {"d": last["d"], "seg": last["seg"]} if last else None,
            "names": SEGMENTS,
        },
    }


def sources_text() -> str:
    """Pie del panel: de dónde salen los datos."""
    weigh = {"fitdays": "pesa Fitdays (API no oficial)", "csv": "pesa (CSV)", "manual": "peso anotado a mano"}
    out = [weigh.get(SOURCES["pesa"], SOURCES["pesa"])]
    if SOURCES["actividad"] != "ninguna":
        out.append("WHOOP" if SOURCES["actividad"] == "whoop" else f"{DEVICE} (CSV)")
    if SOURCES["presion"] != "ninguna":
        out.append("Withings" if SOURCES["presion"] == "withings" else "tensiómetro (CSV)")
    return ", ".join(out[:-1]) + " y " + out[-1] if len(out) > 1 else out[0]


def template_tokens() -> dict[str, str]:
    """Textos de la plantilla que dependen de la persona. Los números van con el formato del panel (decimales con coma; miles con punto)."""
    day = lambda s: date.fromisoformat(s)
    short = lambda d: f"{d.day} {MONTHS[d.month - 1]}"
    dec = lambda v: f"{v:g}".replace(".", ",")
    legend = "\n".join(f'      <span><i class="key-rect" style="background:var({w["color"]})"></i>{w["nombre"]}</span>' for w in WORKOUTS)
    start = day(PLAN_START)
    expense_from = start + timedelta(days=7)
    return {
        "__NOMBRE__": CONFIG["nombre"], "__BASE_1__": short(day(DATA_START)), "__BASE_2__": short(start),
        "__DIA1_CORTO__": f"{start.day}-{start.month}", "__GASTO_DESDE__": f"{expense_from.day}-{expense_from.month}",
        "__META__": f"{dec(PLAN_RULES["goalLow"])}–{dec(PLAN_RULES["goalHigh"])}",
        "__SUBESTIMA__": str(round((1 - 1 / PLAN_RULES["whoopFactor"]) * 100)),
        "__PASOS__": f"{PLAN_RULES["stepsMin"]:,}".replace(",", "."), "__PASOS_NOTA__": CONFIG.get("panel", {}).get("pasos_nota", ""),
        "__HRV_MIN__": dec(PLAN_RULES["hrvMin"]), "__PRESION_HABITUAL__": "{}–{} / {}–{}".format(*PLAN_RULES["bpUsual"]),
        "__LEYENDA_ENTRENOS__": legend, "__DISPOSITIVO__": DEVICE, "__FUENTES__": sources_text(),
        "__META_GRASA__": dec(PLAN_RULES["fatGoal"]),
        "__PRESION_ALTA__": "{}/{}".format(*PLAN_RULES["bpHigh"]), "__PRESION_BAJA__": "{}/{}".format(*PLAN_RULES["bpLow"]),
    }


def main() -> None:
    html = TEMPLATE.read_text()
    for token, text in template_tokens().items():
        html = html.replace(token, text)
    data = json.dumps(build(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(html.replace("__DATA__", data))
    print(f"Panel generado: {OUT.relative_to(ROOT) if OUT.is_relative_to(ROOT) else OUT}")


if __name__ == "__main__":
    main()
