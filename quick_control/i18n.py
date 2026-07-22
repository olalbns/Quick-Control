from __future__ import annotations
import gettext
from pathlib import Path

DOMAIN = "quick-control"
_translation: gettext.NullTranslations | gettext.GNUTranslations = gettext.NullTranslations()


def setup_i18n() -> None:
    global _translation
    candidates = (Path(__file__).resolve().parent.parent / "locale", Path("/usr/share/locale"))
    _translation = gettext.NullTranslations()
    for directory in candidates:
        found = gettext.translation(DOMAIN, localedir=str(directory), fallback=True)
        if type(found) is not gettext.NullTranslations:
            _translation = found
            break


def _(message: str) -> str:
    return _translation.gettext(message)
