# Quick Control

A compact **GTK4 control center** for Linux. Quick Control gives direct access
to everyday desktop settings in a small window, with a focus on Hyprland and
other modern Linux sessions. It uses established system tools rather than
running as root.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform: Linux](https://img.shields.io/badge/Platform-Linux-FCC624.svg)

## Features

- **Wi-Fi** — show NetworkManager status and active SSID; toggle Wi-Fi.
- **Bluetooth** — show power/connection status; toggle Bluetooth.
- **Audio** — show and mute the default PipeWire speaker and microphone.
- **Screen brightness** — a responsive 0–100% slider.
- **Keyboard backlight** — automatic `brightnessctl` detection and 0–100%
  slider for compatible keyboards (for example `dell::kbd_backlight`).
- **Battery** — charge percentage and charging/discharging state.
- **Session actions** — lock, suspend, reboot, or power off (destructive
  actions ask for confirmation).
- **Graceful fallback** — unavailable hardware or tools disable only their
  corresponding card; the rest of the control center keeps working.

## Installation on Arch Linux

### AUR (recommended)

Once the package has been published to the AUR:

```bash
yay -S quick-control-git
```

Install the optional integrations you want:

```bash
sudo pacman -S networkmanager bluez-utils wireplumber brightnessctl upower hyprlock
```

Restart the app after installing an integration.

### Build from source

```bash
git clone https://github.com/olalbns/Quick-Control.git
cd Quick-Control
sudo pacman -S --needed python python-gobject gtk4
PYTHONPATH=. python -m quick_control.app
```

For development on Arch, use a virtual environment or a package build rather
than installing directly into the system Python environment.

## Hyprland shortcut

Add this line to `~/.config/hypr/hyprland.conf` after installing the package:

```ini
bind = SUPER, A, exec, quick-control
```

Then reload Hyprland’s configuration:

```bash
hyprctl reload
```

## Required and optional components

Quick Control itself needs Python, GTK4, and PyGObject. Individual cards use
optional system programs:

| Card | Program / Arch package |
|---|---|
| Wi-Fi | `nmcli` / `networkmanager` |
| Bluetooth | `bluetoothctl` / `bluez-utils` |
| Sound and microphone | `wpctl` / `wireplumber` |
| Screen and keyboard brightness | `brightnessctl` / `brightnessctl` |
| Battery | `upower` / `upower` |
| Hyprland lock screen | `hyprlock` / `hyprlock` |

## Brightness troubleshooting

Check the devices exposed by your hardware:

```bash
brightnessctl -l
```

Quick Control searches for a device with class `backlight` for the display and
an LED whose name includes `kbd` or `keyboard` for the keyboard backlight.
For example, the following device is recognised automatically:

```text
dell::kbd_backlight
```

If the sliders do not react, test the underlying commands:

```bash
brightnessctl set 80%
brightnessctl -d dell::kbd_backlight set 50%
```

If these commands need elevated privileges, configure the appropriate udev
rules for your hardware instead of running the application as root.

## Security and privacy

- Quick Control never requests or stores passwords.
- It does not run as root.
- System actions are submitted to `systemctl`; your desktop’s polkit policy
  determines whether authorization is required.
- No telemetry or network service is included.

## Development

The source is organised as follows:

```text
quick_control/app.py     GTK4 interface
quick_control/system.py  Safe adapters for Linux system tools
data/                    Desktop launcher
aur/quick-control-git/   AUR packaging files
```

Please open an issue with your `brightnessctl -l` output (removing any
sensitive device names if desired) if keyboard backlight detection needs to
support another device naming convention.

## License

[MIT](LICENSE)
