import os
import sys

app_n = "Boxing-CLI"

pkg_dir = os.path.dirname(os.path.abspath(__file__))
_is_pkg = os.path.isfile(os.path.join(pkg_dir, "__init__.py"))
root = os.path.dirname(pkg_dir) if _is_pkg else pkg_dir

def _installed():
    p = pkg_dir.replace("\\", "/").lower()
    return "site-packages" in p or "dist-packages" in p

def _user_dir():
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, app_n)
    return os.path.join(os.path.expanduser("~"), "." + APP_NAME)

def _data_dir():
    override = os.environ.get("BOXING_HOME")
    if override:
        return override
    if getattr(sys, "frozen", False) or _installed():
        return _user_dir()
    return root

data_dir = _data_dir()
try:
    os.makedirs(data_dir, exist_ok=True)
except OSError:
    pass

_assets = os.path.join(pkg_dir, "assets")
assets_dir = _assets if os.path.isdir(_assets) else pkg_dir

def asset(name):
    return os.path.join(assets_dir, name)

saves_dir = os.path.join(data_dir, "saves")
setting_file = os.path.join(data_dir, "settings.json")
legacy_stats = os.path.join(data_dir, "player_stats.json")