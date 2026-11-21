import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    if os.environ.get("VERCEL"):
        return

    explicit_path = os.environ.get("MOVIEBOX_ENV_FILE")
    if explicit_path:
        load_dotenv(Path(explicit_path).expanduser(), override=False)
        return

    try:
        default_home = Path.home()
    except Exception:
        default_home = Path("/tmp")

    config_home = Path(os.environ.get("XDG_CONFIG_HOME", default_home / ".config"))
    candidates = (
        Path.cwd() / ".env",
        config_home / "moviebox" / ".env",
        Path(__file__).resolve().parent / ".env",
    )
    for path in candidates:
        if path.is_file():
            load_dotenv(path, override=False)
            return
