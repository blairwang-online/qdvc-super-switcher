# qdvc-super-switcher

**Quick and dirty vibe-coded (QDVC)** Super+N window switching for MATE, the way GNOME and Windows do it.

On GNOME and Windows, <kbd>Super</kbd>+<kbd>1</kbd> … <kbd>Super</kbd>+<kbd>9</kbd> jump straight to the 1st … 9th window in the taskbar. MATE has no equivalent. This is a small Python script that fills the gap: bind each <kbd>Super</kbd>+<kbd>N</kbd> to `super_switcher.py N`, and it activates the Nth window in panel order using `xdotool`.

Vibe-coding details in [vibe-coding/](https://github.com/blairwang-online/qdvc-super-switcher/blob/main/vibe-coding)

> [!IMPORTANT]
> **This tool numbers windows by their order in `_NET_CLIENT_LIST`, not by their live position in the taskbar.**
>
> - ✅ **It copes with windows closing.** Survivors keep their relative order and shift up to fill the gaps, so the numbering stays sensible.
> - ❌ **It does *not* cope with windows being manually reordered.** Dragging taskbar buttons around changes their visual position but not their `_NET_CLIENT_LIST` order, so the numbers will no longer match what you see.
>
> **So: don't drag-reorder windows in the MATE taskbar if you want this tool to behave predictably.** If you need a particular set of programs in a particular order for some task — say, quickly flipping between a web browser, a file manager, and a terminal — the simplest approach is to close all windows and then intentionally open the programs you need in the sequence you want.

## Why not wmctrl?

Based on my brief testing on Ubuntu 26.04, it seems that `wmctrl -a` isn't working for me, so this uses `xdotool windowactivate` instead.

## Requirements

- MATE (X11)
- `xprop` (usually preinstalled via `x11-utils`)
- `xdotool` — `sudo apt install xdotool`

## Install

```
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
