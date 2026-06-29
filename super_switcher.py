#!/usr/bin/env python3
import subprocess
import sys

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def get_current_desktop():
    # _NET_CURRENT_DESKTOP
    out = sh(["xprop", "-root", "_NET_CURRENT_DESKTOP"])
    return int(out.split("=")[1].strip())

def get_window_list():
    # _NET_CLIENT_LIST_STACKING is stacking order; we want creation/taskbar order
    # _NET_CLIENT_LIST gives initial-mapping order, which matches taskbar order on MATE
    out = sh(["xprop", "-root", "_NET_CLIENT_LIST"])
    # e.g. "_NET_CLIENT_LIST(WINDOW): window id # 0x..., 0x..., ..."
    ids = out.split("#", 1)[1]
    return [w.strip() for w in ids.split(",") if w.strip()]

def get_long(wid, prop):
    out = sh(["xprop", "-id", wid, prop])
    if "=" not in out:
        return None
    return out.split("=")[1].strip()

def is_normal_window(wid):
    # Skip docks, panels, desktop, etc.
    wtype = get_long(wid, "_NET_WM_WINDOW_TYPE") or ""
    if "_NET_WM_WINDOW_TYPE_NORMAL" in wtype:
        return True
    # Many normal windows have no _NET_WM_WINDOW_TYPE set; accept those too
    if wtype == "" or wtype == "not found.":
        return True
    return False

def is_skip_taskbar(wid):
    state = get_long(wid, "_NET_WM_STATE") or ""
    return "_NET_WM_STATE_SKIP_TASKBAR" in state

def get_desktop(wid):
    val = get_long(wid, "_NET_WM_DESKTOP")
    if val is None or "not found" in val:
        return None
    try:
        return int(val.split()[0].split(",")[0])
    except ValueError:
        return None

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: super_switcher.py N")
    try:
        n = int(sys.argv[1])
    except ValueError:
        sys.exit("argument must be an integer 1-9")
    if n < 1:
        sys.exit("argument must be >= 1")

    current = get_current_desktop()
    windows = []
    for wid in get_window_list():
        if not is_normal_window(wid):
            continue
        if is_skip_taskbar(wid):
            continue
        d = get_desktop(wid)
        # 0xFFFFFFFF (-1 / sticky) shows on all desktops
        if d is not None and d != current and d != 0xFFFFFFFF:
            continue
        windows.append(wid)

    if n > len(windows):
        return  # nothing in that slot
    target = windows[n - 1]
    subprocess.run(["xdotool", "windowactivate", target])

if __name__ == "__main__":
    main()
