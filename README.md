# Quick Control

Centre de contrôle GTK4 compact pour Hyprland et les bureaux Linux modernes.

## Fonctions

- Wi-Fi et Bluetooth ;
- volume et microphone PipeWire ;
- curseurs de luminosité de l’écran et du clavier ;
- batterie ;
- verrouillage, suspension, redémarrage et arrêt ;
- actualisation automatique des états.

Les cartes dont le matériel ou l’outil système est absent sont désactivées sans
empêcher les autres fonctions de fonctionner.

## Installation sur Arch Linux

```bash
yay -S quick-control-git
```

Installez les intégrations que vous souhaitez utiliser :

```bash
sudo pacman -S networkmanager bluez-utils wireplumber brightnessctl upower hyprlock
```

Selon le matériel, l’accès à la luminosité peut demander une règle udev ou
l’appartenance au groupe `video`.

## Utilisation

Lancez Quick Control depuis le menu d’applications ou avec :

```bash
quick-control
```

Raccourci Hyprland conseillé :

```ini
bind = SUPER, A, exec, quick-control
```

Pour vérifier les rétroéclairages disponibles :

```bash
brightnessctl -l
```
