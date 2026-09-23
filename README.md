# Zaryadka

A minimalist 10-minute calisthenics coach. It's a single static page with no build step and no dependencies.

- Queues the workouts in [`workouts.json`](workouts.json) in order. Hit **Start**, or **Skip** to move to the next one
- **Rep sets** show a target and a big *Done* button. **Hold sets** and **rest** are timed, with a 3-2-1 beep countdown
- Beeps, optional voice announcements ("Rest. Next, push-ups"), and it keeps the screen awake during a session
- Turn on **Mic “done”** and say *done* to finish a rep set without touching the phone. It's the only command, and it only listens during a session
- History is stored on the device, shown as a small calendar grid, and can be exported or imported as a JSON file
- Tap any day in the grid to log a workout you did away from the app, or to remove one logged by mistake
- Works offline and installs to the home screen

Edit workouts yourself or with an agent. See [AGENTS.md](AGENTS.md), then run `python3 check.py`.

## Run locally
```bash
python3 -m http.server 8765
```
Open http://localhost:8765. For a quick test, http://localhost:8765/?speed=20 runs the timers 20× faster.

## Host on GitHub Pages (free)
```bash
git init && git add -A && git commit -m "Zaryadka"
gh repo create zaryadka --public --source=. --push
gh api -X POST repos/{owner}/zaryadka/pages -f "source[branch]=main" -f "source[path]=/"
```
The app will be at `https://<username>.github.io/zaryadka/`. After that, every push to `main` redeploys it.
Free GitHub Pages needs a public repo. Nothing personal is in it, since your history stays on your devices.

## Install
- **Android (Chrome):** open the URL, then ⋮ → *Add to Home screen* / *Install app*. It runs fullscreen with its own icon and works offline.
- **iPhone (Safari):** Share → *Add to Home Screen*. Turn off silent mode, or the beeps won't play.
- **Laptop (Chrome/Edge):** use the install icon in the address bar, or just keep a tab open.

## Tracking and sync
Each device keeps its own log in browser storage. Use **Export log** to save a JSON file (to Downloads, Drive, and so on) and **Import log** to merge one in, for example to move history from your phone to your laptop. Imports are de-duplicated.
