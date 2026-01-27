"""
Best-effort helper to set the STEAM_EXTERNAL_OVERLAY atom on an X11 window.

This implementation deliberately avoids adding a new Python dependency and
uses the system `xprop` tool if present. Behavior is best-effort and failures
are logged only.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from typing import Optional


def set_steam_external_overlay_atom(winid: int, logger: Optional[logging.Logger] = None) -> bool:
    """
    Attempt to set the STEAM_EXTERNAL_OVERLAY property on the X11 window `winid`.
    Returns True on success, False on failure.
    Uses the `xprop` command if available. Does not raise.
    """
    log = logger or logging.getLogger(__name__)
    win_str = str(int(winid))

    xprop = shutil.which("xprop")
    if not xprop:
        log.debug("xprop not found on PATH; cannot set STEAM_EXTERNAL_OVERLAY")
        return False

    try:
        # Use 32-bit cardinal and set value to 1
        subprocess.check_call(
            [xprop, "-id", win_str, "-f", "STEAM_EXTERNAL_OVERLAY", "32c", "-set", "STEAM_EXTERNAL_OVERLAY", "1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log.info("Set STEAM_EXTERNAL_OVERLAY on X11 window %s via xprop", win_str)
        return True
    except Exception as exc:
        log.debug("xprop failed to set STEAM_EXTERNAL_OVERLAY on %s: %s", win_str, exc)
        return False