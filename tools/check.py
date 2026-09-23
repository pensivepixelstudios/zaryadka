#!/usr/bin/env python3
"""Validate data/workouts.json and print a summary of each workout. Usage: python3 tools/check.py"""
import json, pathlib, sys

path = pathlib.Path(__file__).resolve().parent.parent / "data" / "workouts.json"
try:
    c = json.loads(path.read_text())
except json.JSONDecodeError as e:
    sys.exit(f"✗ data/workouts.json is not valid JSON: {e}")

errs, ids = [], set()
ex = c.get("exercises") or {}
for k, x in ex.items():
    if not isinstance(x, dict) or not x.get("name"):
        errs.append(f'exercise "{k}": missing "name"')
    elif x.get("type", "hold") not in ("reps", "hold", "stopwatch"):
        errs.append(f'exercise "{k}": type must be "reps", "hold" or "stopwatch"')
ws = c.get("workouts") or []
if not ws:
    errs.append('"workouts" must be a non-empty array')
for i, w in enumerate(ws):
    wid = w.get("id") or f"#{i + 1}"
    if not w.get("id"):
        errs.append(f'workout {wid}: missing "id"')
    elif wid in ids:
        errs.append(f"workout {wid}: duplicate id")
    ids.add(wid)
    if not w.get("intervals"):
        errs.append(f'workout {wid}: "intervals" must be a non-empty array')
    for s in w.get("intervals") or []:
        e = s if isinstance(s, str) else (s or {}).get("ex")
        if e not in ex:
            errs.append(f'workout {wid}: unknown exercise "{e}"')
if errs:
    print("\n".join("✗ " + e for e in errs))
    sys.exit(1)

for w in ws:
    flat = [s for raw in w["intervals"] for s in [{"ex": raw} if isinstance(raw, str) else raw] * (1 if isinstance(raw, str) else raw.get("sets", 1))]
    n = w.get("sets") or len(flat)
    total = w.get("prep", c.get("prep", 10))
    names, open_ = [], False
    for k in range(n):
        s = flat[k % len(flat)]
        x = ex[s["ex"]]
        work = s.get("work", x.get("work", w.get("work", c.get("work", 30))))
        rest = s.get("rest", x.get("rest", w.get("rest", c.get("rest", 30))))
        total += work + (rest if k < n - 1 else 0)
        t = x.get("type", "hold")
        open_ |= t == "stopwatch"
        names.append(f'{x["name"]} ×{s.get("reps", x.get("reps", 10))}' if t == "reps" else f'{x["name"]} (stopwatch)' if t == "stopwatch" else f'{x["name"]} {work}s')
    length = "open-ended" if open_ else f"≈{total // 60}:{total % 60:02d}"
    print(f'✓ {w["id"]:<12} {w.get("name", ""):<16} {n} sets  {length:<10} ' + ", ".join(names))
