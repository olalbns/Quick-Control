# Publishing `quick-control-git` to the AUR

The application source is hosted at <https://github.com/olalbns/Quick-Control>.
The AUR repository contains only `PKGBUILD` and `.SRCINFO`.

## Prerequisites

1. Register at <https://aur.archlinux.org/register/>.
2. Add your public SSH key in **My Account** on the AUR website.
3. Install build tools:

```bash
sudo pacman -S --needed base-devel git openssh
```

## Test the package

From this project’s root:

```bash
cd aur/quick-control-git
rm -rf src pkg
makepkg -si
makepkg --printsrcinfo > .SRCINFO
```

## First publication

The AUR accepts pushes only to the `master` branch:

```bash
project_dir="$HOME/Quick-Control"
git clone ssh://aur@aur.archlinux.org/quick-control-git.git /tmp/quick-control-git-aur
cp "$project_dir/aur/quick-control-git/PKGBUILD" /tmp/quick-control-git-aur/
cp "$project_dir/aur/quick-control-git/.SRCINFO" /tmp/quick-control-git-aur/
cd /tmp/quick-control-git-aur
git checkout -B master
git add PKGBUILD .SRCINFO
git commit -m 'Initial AUR package'
git push -u origin master
```

After the AUR indexes the package, users can install it with:

```bash
yay -S quick-control-git
```

## Updating the AUR package

After pushing application changes to GitHub, regenerate `.SRCINFO`, commit the
changed package files in the AUR clone, and push its `master` branch:

```bash
cd "$HOME/Quick-Control/aur/quick-control-git"
makepkg --printsrcinfo > .SRCINFO
cp PKGBUILD .SRCINFO /tmp/quick-control-git-aur/
cd /tmp/quick-control-git-aur
git add PKGBUILD .SRCINFO
git commit -m 'Update quick-control-git'
git push
```
