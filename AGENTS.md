# Zaryadka — instructions for agents

Zaryadka is a static, dependency-free workout PWA (`index.html`). The **only file you normally edit is `workouts.json`**.
After any edit, run `python3 check.py` — it validates the file and prints each workout with its estimated length.

## workouts.json

```jsonc
{
  "work": 30,            // default seconds for "hold" sets (also the time estimate for "reps" sets)
  "rest": 30,            // default rest seconds after each set (no rest after the last set)
  "prep": 10,            // "get ready" countdown before the first set

  "exercises": {
    "<id>": {
      "name": "Push-ups",
      "type": "reps",     // "reps": show target, user taps Done  |  "hold": timed countdown
                          // "stopwatch": counts up until the user taps Done (runs, climbs); no reps/work, not in the estimate
      "reps": 10,         // target for "reps" exercises
      "work": 30,         // optional per-exercise hold time / rest override
      "rest": 30
    }
  },

  "workouts": [
    {
      "id": "circuit",               // unique, stable (the log references it)
      "name": "Full Circuit",
      "sets": 10,                    // optional total; "intervals" is cycled until this count (default: all intervals once)
      "work": 30, "rest": 30,        // optional workout-level overrides
      "intervals": [
        { "ex": "pushups", "sets": 5 },             // a block: 5 consecutive sets of push-ups
        { "ex": "squats", "sets": 5, "reps": 12 },  // per-block overrides: sets, work, rest, reps
        "hollow_man"                                // bare exercise id = a single set
      ]
    }
  ]
}
```

Override precedence (most specific wins): interval → exercise → workout → top-level default.

## Guidelines
- The user wants exercises done **in blocks** (all sets of one exercise, then the next), not alternated.
- Keep each workout at **≈10 minutes** (`check.py` shows the estimate). With 30s rest, 10 sets ≈ 10 min.
- Exercise ids: lowercase `snake_case`. Don't rename or reuse existing workout ids — history refers to them.
- Exercises show only their name — don't add form cues or descriptions.
- Workouts form a queue in list order: finishing or skipping one moves to the next (tracked per device). Removing or reordering is fine.
- The app name lives in `index.html` and `manifest.webmanifest`, not here.
- Only `workouts.json` needs to change to add exercises or workouts. Commit and push; GitHub Pages redeploys in about a minute.

## Workout log format (exported by the app, "Export log")
```json
{ "app": "zaryadka", "exported": "…", "log": [
  { "d": "2026-09-11", "t": "2026-09-11T07:02:11.000Z", "w": "circuit", "n": "Full Circuit", "of": 10,
    "sets": [ { "ex": "pushups", "reps": 10, "s": 24 }, { "ex": "hollow_man", "hold": 30, "s": 2, "skipped": true } ] }
] }
```
`s` is the number of seconds the set took (for a stopwatch set, which has no `reps`/`hold`, that is the whole activity, pauses excluded). For rep sets this tells you how fast the user got through the target, which helps when deciding whether to raise `reps`.
`of` is the number of sets planned. Sets marked `"skipped": true` weren't done, and a session ended early lists only the sets reached, so completion = non-skipped sets ÷ `of`. Entries without `of` are complete sessions saved before this was tracked.
`"manual": true` marks a workout that wasn't run: ticked off with "Mark done", or logged by tapping a day in the history grid. Every set is recorded as done with `s: 0`.
