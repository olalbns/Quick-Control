"""Small, defensive adapters around standard Linux desktop commands."""
from __future__ import annotations
import re
import shutil
import subprocess
from dataclasses import dataclass

@dataclass
class State:
    wifi: str = "—"
    bluetooth: str = "—"
    volume: str = "—"
    microphone: str = "—"
    brightness: str = "—"
    battery: str = "—"


def available(command: str) -> bool:
    return shutil.which(command) is not None


def output(*command: str) -> str | None:
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, timeout=8, check=True)
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return None


def run(*command: str) -> bool:
    return output(*command) is not None


def background(*command: str) -> bool:
    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
        return True
    except FileNotFoundError:
        return False


def _switch(value: str, on: bool) -> bool:
    return value.strip().lower() in (("enabled", "yes", "on") if on else ("disabled", "no", "off"))


def wifi_state() -> tuple[bool | None, str]:
    radio = output("nmcli", "radio", "wifi")
    if radio is None: return None, "NetworkManager unavailable"
    enabled = radio.strip().lower() == "enabled"
    if not enabled: return False, "Wi‑Fi off"
    active = output("nmcli", "-t", "-f", "ACTIVE,SSID", "device", "wifi") or ""
    for line in active.splitlines():
        if line.startswith("yes:"):
            return True, line[4:] or "Connected"
    return True, "On — not connected"


def set_wifi(enabled: bool) -> bool:
    return run("nmcli", "radio", "wifi", "on" if enabled else "off")


def bluetooth_state() -> tuple[bool | None, str]:
    info = output("bluetoothctl", "show")
    if info is None: return None, "Bluetooth unavailable"
    powered = re.search(r"^\s*Powered:\s*(yes|no)", info, re.MULTILINE)
    if not powered: return None, "Bluetooth unavailable"
    on = powered.group(1) == "yes"
    if not on: return False, "Bluetooth off"
    connected = output("bluetoothctl", "devices", "Connected") or ""
    device = next((x.split(" ", 2)[-1] for x in connected.splitlines() if x.startswith("Device ")), None)
    return True, device or "On — no device"


def set_bluetooth(enabled: bool) -> bool:
    return run("bluetoothctl", "power", "on" if enabled else "off")


def _audio_state(target: str) -> tuple[bool | None, str]:
    text = output("wpctl", "get-volume", target)
    if text is None: return None, "PipeWire unavailable"
    match = re.search(r"Volume:\s*([0-9.]+)(?:\s+\[MUTED\])?", text)
    if not match: return None, "Unavailable"
    muted = "[MUTED]" in text
    percent = round(float(match.group(1)) * 100)
    return not muted, ("Muted" if muted else f"{percent}%")


def volume_state() -> tuple[bool | None, str]: return _audio_state("@DEFAULT_AUDIO_SINK@")
def microphone_state() -> tuple[bool | None, str]: return _audio_state("@DEFAULT_AUDIO_SOURCE@")
def set_volume(delta: str) -> bool: return run("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", delta)
def toggle_mute(target: str) -> bool: return run("wpctl", "set-mute", target, "toggle")


def _brightness_percent(*args: str) -> int | None:
    text = output("brightnessctl", *args, "-m")
    if text is None: return None
    # brightnessctl -m emits: device,class,current,max (not a percentage).
    # Device names may contain escaped commas, so only inspect the last fields.
    fields = text.rsplit(",", 2)
    if len(fields) != 3: return None
    try:
        current, maximum = int(fields[1]), int(fields[2])
        return round(current * 100 / maximum) if maximum else None
    except ValueError:
        return None


def brightness_state() -> tuple[int | None, str]:
    level = _brightness_percent()
    return (level, f"{level}%") if level is not None else (None, "Brightness control unavailable")


def set_brightness(percent: int) -> bool:
    return run("brightnessctl", "set", f"{max(0, min(100, percent))}%")


def keyboard_backlight_device() -> str | None:
    """Return a keyboard-backlight LED accepted by brightnessctl, if present."""
    devices = output("brightnessctl", "-l") or ""
    for line in devices.splitlines():
        # brightnessctl uses quotation marks that vary between releases/fonts.
        # Splitting the stable parts is more reliable than matching the quote.
        if "Device" not in line or "of class 'leds'" not in line:
            continue
        name = line.split("Device", 1)[1].split("of class", 1)[0].strip(" `\"'")
        lowered = name.lower()
        if "kbd" in lowered or "keyboard" in lowered:
            return name
    return None


def keyboard_brightness_state() -> tuple[int | None, str]:
    device = keyboard_backlight_device()
    if not device:
        return None, "Keyboard backlight unavailable"
    level = _brightness_percent("-d", device)
    return (level, f"{level}% · {device}") if level is not None else (None, "Keyboard backlight unavailable")


def set_keyboard_brightness(percent: int) -> bool:
    device = keyboard_backlight_device()
    return bool(device) and run("brightnessctl", "-d", device, "set", f"{max(0, min(100, percent))}%")


def battery_state() -> tuple[bool | None, str]:
    devices = output("upower", "-e")
    if devices is None: return None, "Battery unavailable"
    battery = next((line for line in devices.splitlines() if "battery" in line.lower()), None)
    if not battery: return None, "No battery"
    info = output("upower", "-i", battery) or ""
    percent = re.search(r"^\s*percentage:\s*(.+)$", info, re.MULTILINE)
    status = re.search(r"^\s*state:\s*(.+)$", info, re.MULTILINE)
    return True, f"{percent.group(1).strip() if percent else '—'} · {status.group(1).strip() if status else ''}"


def lock() -> bool:
    # loginctl is a safe fallback where hyprlock is not installed.
    return background("hyprlock") if available("hyprlock") else run("loginctl", "lock-session")
