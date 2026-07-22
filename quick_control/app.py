from __future__ import annotations
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk
from .i18n import _, setup_i18n
from . import system

APP_ID = "io.github.olalbns.quickcontrol"

class Card(Gtk.Box):
    def __init__(self, title: str, icon: str, callback):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.add_css_class("card")
        row = Gtk.Box(spacing=10)
        glyph = Gtk.Label(label=icon); glyph.add_css_class("title-2")
        labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, hexpand=True)
        self.title = Gtk.Label(label=title, xalign=0)
        self.detail = Gtk.Label(label="—", xalign=0); self.detail.add_css_class("dim-label")
        labels.append(self.title); labels.append(self.detail)
        self.switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.switch.connect("state-set", self.on_switch, callback)
        row.append(glyph); row.append(labels); row.append(self.switch); self.append(row)

    def on_switch(self, _switch, value, callback):
        callback(value)
        return False

    def update(self, value: bool | None, detail: str):
        self.detail.set_text(detail)
        self.switch.set_sensitive(value is not None)
        if value is not None:
            self.switch.set_state(value)

class Window(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application):
        super().__init__(application=app, title=_("Quick Control"))
        self.set_default_size(480, 570)
        self.set_resizable(False)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14,
                       margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)
        self.set_child(main)
        title = Gtk.Label(label=_("Quick Control"), xalign=0); title.add_css_class("title-1")
        main.append(title)
        subtitle = Gtk.Label(label=_("Controls for the current desktop session"), xalign=0)
        subtitle.add_css_class("dim-label"); main.append(subtitle)
        grid = Gtk.Grid(column_spacing=12, row_spacing=12, column_homogeneous=True)
        main.append(grid)
        self.wifi = Card(_("Wi‑Fi"), "⌁", self.change_wifi)
        self.bluetooth = Card(_("Bluetooth"), "ᛒ", self.change_bluetooth)
        self.volume = Card(_("Sound"), "🔊", self.change_volume_mute)
        self.microphone = Card(_("Microphone"), "🎙", self.change_microphone_mute)
        self.brightness = Card(_("Brightness"), "☀", self.change_brightness)
        self.battery = Card(_("Battery"), "▰", lambda _v: None)
        self.battery.switch.set_visible(False)
        for index, card in enumerate((self.wifi, self.bluetooth, self.volume, self.microphone, self.brightness, self.battery)):
            grid.attach(card, index % 2, index // 2, 1, 1)
        actions = Gtk.Box(spacing=8, homogeneous=True, margin_top=4)
        main.append(actions)
        for text, icon, callback in ((_("Lock"), "🔒", self.do_lock), (_("Suspend"), "⏾", lambda: self.confirm("suspend")),
                                     (_("Restart"), "↻", lambda: self.confirm("reboot")), (_("Power off"), "⏻", lambda: self.confirm("poweroff"))):
            button = Gtk.Button(label=f"{icon}  {text}"); button.connect("clicked", lambda _b, f=callback: f()); actions.append(button)
        self.status = Gtk.Label(label=_("Ready."), xalign=0); self.status.add_css_class("dim-label"); main.append(self.status)
        self.refresh()
        GLib.timeout_add_seconds(5, self.refresh)

    def action(self, ok: bool, message: str):
        self.status.set_text(message if ok else _("Action was not permitted or the required tool is unavailable."))
        self.refresh()

    def change_wifi(self, enabled): self.action(system.set_wifi(enabled), _("Wi‑Fi updated."))
    def change_bluetooth(self, enabled): self.action(system.set_bluetooth(enabled), _("Bluetooth updated."))
    def change_volume_mute(self, _enabled): self.action(system.toggle_mute("@DEFAULT_AUDIO_SINK@"), _("Sound updated."))
    def change_microphone_mute(self, _enabled): self.action(system.toggle_mute("@DEFAULT_AUDIO_SOURCE@"), _("Microphone updated."))
    def change_brightness(self, enabled): self.action(system.set_brightness("+5%" if enabled else "5%-"), _("Brightness updated."))
    def do_lock(self): self.action(system.lock(), _("Session locked."))

    def confirm(self, action: str):
        labels = {"suspend": _("Suspend"), "reboot": _("Restart"), "poweroff": _("Power off")}
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, buttons=Gtk.ButtonsType.CANCEL,
                                   text=_("Confirm action"), secondary_text=_("Do you really want to {}?").format(labels[action].lower()))
        dialog.add_button(labels[action], Gtk.ResponseType.ACCEPT)
        dialog.connect("response", lambda d, response: (d.destroy(), system.run("systemctl", action) if response == Gtk.ResponseType.ACCEPT else None))
        dialog.present()

    def refresh(self):
        self.wifi.update(*system.wifi_state())
        self.bluetooth.update(*system.bluetooth_state())
        self.volume.update(*system.volume_state())
        self.microphone.update(*system.microphone_state())
        self.brightness.update(*system.brightness_state())
        self.battery.update(*system.battery_state())
        return True

class App(Gtk.Application):
    def __init__(self): super().__init__(application_id=APP_ID)
    def do_activate(self):
        (self.props.active_window or Window(self)).present()

def main():
    setup_i18n(); App().run(None)
if __name__ == "__main__": main()
