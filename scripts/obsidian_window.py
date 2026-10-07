#!/usr/bin/env python3
"""Start, control, and stop a temporary Obsidian window for tests that need the real app.

Usage:
  python3 scripts/obsidian_window.py start [--mode light|dark] [--port 9333] [--dir DIR]
  python3 scripts/obsidian_window.py status
  python3 scripts/obsidian_window.py reload             copy the theme files again and reload the CSS
  python3 scripts/obsidian_window.py theme light|dark   switch the mode
  python3 scripts/obsidian_window.py open NOTE [preview|source]
  python3 scripts/obsidian_window.py eval 'JS EXPRESSION'
  python3 scripts/obsidian_window.py shot FILE [WIDTHxHEIGHT]
  python3 scripts/obsidian_window.py run SCRIPT.mjs     run a script for scripts/cdp.mjs
  python3 scripts/obsidian_window.py stop [--clean]

A window shows on your screen while it runs. The script makes a demo vault with a Showcase note
and a profile folder in DIR (default /tmp/lexmechanic-window), starts Obsidian with that profile and
a debug port, and keeps the window until `stop`. It never uses your own profile or vault. `stop`
stops only the process group that `start` made, and tells whether the config and the vaults of
your own Obsidian changed while the window ran. Use one window for a whole batch of checks.
OBSIDIAN_CMD sets the command, if `obsidian` is not on PATH. docs/testing.md has the details.
It needs Node 22 or newer, and it uses only the Python standard library.
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_obsidian_css import find_asar  # noqa: E402
import make_demo_vault  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = Path(os.environ.get("LEXMECHANIC_WINDOW_DIR", "/tmp/lexmechanic-window"))
# Chromium pauses the animation and the timers of a window that is hidden or covered. The graph needs them.
FLAGS = ["--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows", "--disable-background-timer-throttling"]


def build_command(obsidian, profile, port):
    """Return the command that starts Obsidian with its own profile folder and a debug port."""
    return [*obsidian, f"--user-data-dir={profile}", f"--remote-debugging-port={port}", "--remote-allow-origins=*", *FLAGS]


def other_obsidian_processes(ps_text, profile):
    """Count the Obsidian processes in `ps` output that do not use the given profile folder."""
    return sum(1 for line in ps_text.splitlines() if "app.asar" in line and str(profile) not in line and "obsidian_window" not in line)


def watched_files(config_dir):
    """Return the config file of the user's Obsidian and the JSON files of its vaults, for a before and after check."""
    files = [config_dir / "obsidian.json"]
    try:
        for vault in json.loads(files[0].read_text()).get("vaults", {}).values():
            files += sorted((Path(vault["path"]) / ".obsidian").glob("*.json"))
    except (OSError, ValueError, KeyError):
        pass
    return files


def mtimes(files):
    return {str(f): (f.stat().st_mtime_ns if f.exists() else None) for f in files}


def config_dir():
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "obsidian"


def state_file(directory):
    return Path(directory) / "window.json"


def read_state(directory):
    try:
        return json.loads(state_file(directory).read_text())
    except (OSError, ValueError):
        return None


def alive(state):
    """True when the process group that start made still has its leader."""
    try:
        args = Path(f"/proc/{state['pgid']}/cmdline").read_bytes().decode(errors="ignore")
    except OSError:
        return False
    return state["profile"] in args


def js(directory, port, body, target=None):
    """Run JavaScript body through scripts/cdp.mjs. The body has ev, shot, sleep, and send.
    With target, the body runs in the window whose title has that text, such as Settings."""
    task = Path(directory) / "task.mjs"
    task.write_text("export default async ({ ev, shot, sleep, send }) => {\n" + body + "\n};\n")
    env = {**os.environ, "CDP_TARGET": target} if target else None
    result = subprocess.run(["node", str(ROOT / "scripts" / "cdp.mjs"), str(task), str(port)], capture_output=True, text=True, timeout=300, env=env)
    if result.returncode:
        sys.exit(result.stderr.strip() or "the script failed")
    return result.stdout


def start(args):
    directory = Path(args.get("--dir", DEFAULT_DIR))
    port = int(args.get("--port", 9333))
    mode = args.get("--mode", "light")
    state = read_state(directory)
    if state and alive(state):
        sys.exit(f"A window is running (process group {state['pgid']}). Run stop first.")
    shutil.rmtree(directory, ignore_errors=True)
    vault, profile = directory / "vault", directory / "profile"
    profile.mkdir(parents=True)
    make_demo_vault.build(vault, 30, mode, showcase=True)
    subprocess.run([str(ROOT / "scripts" / "install.sh"), str(vault), "--presets"], check=True, capture_output=True)
    shutil.copy(find_asar(), profile)
    (profile / "obsidian.json").write_text(json.dumps({"vaults": {"lexwindow0000001": {"path": str(vault), "ts": int(time.time() * 1000), "open": True}}}))
    ps = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout
    others = other_obsidian_processes(ps, profile)
    before = mtimes(watched_files(config_dir()))
    obsidian = os.environ.get("OBSIDIAN_CMD", shutil.which("obsidian") or "").split()
    if not obsidian:
        sys.exit("Obsidian was not found. Set OBSIDIAN_CMD to the command that starts it.")
    log = open(directory / "obsidian.log", "w")
    process = subprocess.Popen(build_command(obsidian, profile, port), stdout=log, stderr=log, start_new_session=True)
    state = {"pgid": process.pid, "profile": str(profile), "port": port, "vault": str(vault), "before": before, "dir": str(directory)}
    state_file(directory).write_text(json.dumps(state))
    for _ in range(120):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
            break
        except OSError:
            time.sleep(0.5)
    else:
        stop({"--dir": str(directory)})
        sys.exit("The debug port did not answer in 60 seconds.")
    js(directory, port, "for (let i = 0; i < 80; i++) { if (await ev('!!(window.app && app.workspace && app.workspace.layoutReady)') === true) break; await sleep(500); }\n"
       "await ev(\"document.querySelectorAll('.modal-close-button').forEach(b => b.click())\");")
    print(f"window ready: process group {process.pid}, port {port}, vault {vault}")
    if others:
        print(f"note: {others} other Obsidian process(es) run. This script does not touch them.")


def stop(args):
    directory = Path(args.get("--dir", DEFAULT_DIR))
    state = read_state(directory)
    if not state:
        print("no window state found")
        return
    if alive(state):
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(state["pgid"], sig)
            except ProcessLookupError:
                break
            for _ in range(20):
                if not alive(state):
                    break
                time.sleep(0.25)
            if not alive(state):
                break
    after = mtimes(watched_files(config_dir()))
    changed = [f for f in after if after[f] != state["before"].get(f)]
    print("window stopped. Your own Obsidian config and vault files " + ("did not change." if not changed else "CHANGED: " + ", ".join(changed)))
    if "--clean" in args:
        shutil.rmtree(directory, ignore_errors=True)
        print(f"deleted {directory}")
    else:
        state_file(directory).unlink(missing_ok=True)


def need_state(args):
    state = read_state(Path(args.get("--dir", DEFAULT_DIR)))
    if not state or not alive(state):
        sys.exit("No window is running. Run start first.")
    return state


def parse(argv):
    args, rest, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ("--dir", "--port", "--mode"):
            args[argv[i]] = argv[i + 1]
            i += 2
        elif argv[i] == "--clean":
            args["--clean"] = True
            i += 1
        else:
            rest.append(argv[i])
            i += 1
    return args, rest


RELOAD = "await ev('app.customCss.requestLoadTheme(); app.customCss.requestLoadSnippets(); 0'); await sleep(1200);"


def main(argv):
    args, rest = parse(argv)
    if not rest or rest[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    command, rest = rest[0], rest[1:]
    if command == "start":
        start(args)
    elif command == "stop":
        stop(args)
    elif command == "status":
        state = read_state(Path(args.get("--dir", DEFAULT_DIR)))
        print(json.dumps({k: v for k, v in (state or {}).items() if k != "before"}) + (" alive" if state and alive(state) else " not running"))
    else:
        state = need_state(args)
        port, directory = state["port"], state["dir"]
        if command == "reload":
            subprocess.run([str(ROOT / "scripts" / "install.sh"), state["vault"], "--presets"], check=True, capture_output=True)
            js(directory, port, RELOAD)
        elif command == "theme":
            name = "obsidian" if rest[0] == "dark" else "moonstone"
            js(directory, port, f"await ev({json.dumps(f'app.changeTheme({chr(39)}{name}{chr(39)}); 0')}); await sleep(1000);")
        elif command == "open":
            mode = rest[1] if len(rest) > 1 else "preview"
            view = {"type": "markdown", "state": {"file": rest[0] + ".md", "mode": mode, "source": False}, "active": True}
            call = "(async () => { await app.workspace.getLeaf(false).setViewState(" + json.dumps(view) + "); return 0; })()"
            js(directory, port, f"await ev({json.dumps(call)});\nawait sleep(1200);")
        elif command == "eval":
            print(js(directory, port, f"console.log(JSON.stringify(await ev({json.dumps(rest[0])})));").strip())
        elif command == "shot":
            size = rest[1].split("x") if len(rest) > 1 else ["1280", "800"]
            js(directory, port, f"await send('Emulation.setDeviceMetricsOverride', {{width: {size[0]}, height: {size[1]}, deviceScaleFactor: 1, mobile: false}});\n"
               f"await sleep(600);\nawait shot({json.dumps(str(Path(rest[0]).resolve()))});")
        elif command == "run":
            print(subprocess.run(["node", str(ROOT / "scripts" / "cdp.mjs"), str(Path(rest[0]).resolve()), str(port)], capture_output=True, text=True, timeout=600).stdout.strip())
        else:
            sys.exit(f"unknown command {command}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
