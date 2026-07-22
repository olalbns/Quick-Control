# Quick Control

Centre de contrôle GTK4 compact pour Linux. Il fonctionne dans une session
Hyprland et peut aussi fonctionner dans tout autre environnement utilisant les
outils système compatibles.

## Première version

- Wi‑Fi : état, réseau actif et interrupteur (`NetworkManager` / `nmcli`)
- Bluetooth : état et appareil connecté (`bluez-utils` / `bluetoothctl`)
- Son et microphone : volume ou activation du son (`PipeWire` / `wpctl`)
- Luminosité : état et interruption pour augmenter/réduire (`brightnessctl`)
- Batterie (`upower`)
- Verrouillage, suspension, redémarrage et arrêt avec confirmation
- Actualisation automatique toutes les 5 secondes

## Dépendances Arch Linux

```bash
sudo pacman -S python python-gobject gtk4 networkmanager bluez-utils \
  pipewire brightnessctl upower
```

`hyprlock` est recommandé pour le verrouillage sous Hyprland. Les opérations
sur la luminosité peuvent nécessiter d’ajouter l’utilisateur au groupe `video`
selon le matériel et la configuration udev.

## Lancement depuis les sources

```bash
cd quick-control
PYTHONPATH=. python -m quick_control.app
```

## Raccourci Hyprland

Ajoutez à `~/.config/hypr/hyprland.conf` :

```ini
bind = SUPER, A, exec, quick-control
```

## Luminosité écran et clavier

Les deux luminosités sont contrôlées par des curseurs de 0 à 100 %. Le clavier
est détecté automatiquement parmi les périphériques LED de `brightnessctl`
(noms contenant `kbd` ou `keyboard`, par exemple `asus::kbd_backlight`). Si le
clavier ne possède pas de rétroéclairage compatible, son curseur est désactivé.
