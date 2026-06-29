# qdvc-super-switcher

**Quick and dirty vibe-coded (QDVC)** Super+N window switching for MATE, the way GNOME and Windows do it.

On GNOME and Windows, <kbd>Super</kbd>+<kbd>1</kbd> … <kbd>Super</kbd>+<kbd>9</kbd> jump straight to the 1st … 9th window in the taskbar. MATE has no equivalent. This is a small Python script that fills the gap: bind each <kbd>Super</kbd>+<kbd>N</kbd> to `super_switcher.py N`, and it activates the Nth window in panel order using `xdotool`.

Vibe-coding details in [vibe-coding/](vibe-coding/)

## Why not wmctrl?

Based on my brief testing on Ubuntu 26.04, it seems that `wmctrl -a` isn't working for me, so this uses `xdotool windowactivate` instead.

## Requirements

- MATE (X11)
- `xprop` (usually preinstalled via `x11-utils`)
- `xdotool` — `sudo apt install xdotool`

## Install

```bash
chmod +x super_switcher.py
```

## Set up the shortcuts

Open **System → Preferences → Hardware → Keyboard Shortcuts**, then add custom shortcuts:

| Shortcut | Command |
| --- | --- |
| <kbd>Super</kbd>+<kbd>1</kbd> | `/path/to/super_switcher.py 1` |
| <kbd>Super</kbd>+<kbd>2</kbd> | `/path/to/super_switcher.py 2` |
| … | … |
| <kbd>Super</kbd>+<kbd>9</kbd> | `/path/to/super_switcher.py 9` |

## How it works

Window order is read from the `_NET_CLIENT_LIST` root property (initial-mapping order), which matches the order the Window List applet uses. The script filters out docks, panels, and taskbar-excluded windows, and by default limits results to the current workspace plus sticky windows.

If your panel is configured to show windows from **all** workspaces, remove the desktop-filtering block so the numbering stays in sync with the panel.
