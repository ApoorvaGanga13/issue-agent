import os

from defaults import DEFAULTS

TRUE_VALUES = {"true", "1", "yes"}


def _convert(value, default):
    if isinstance(default, bool):
        return value.strip().lower() in TRUE_VALUES
    if isinstance(default, int):
        return int(value)
    return value


def load(env=None):
    env = os.environ if env is None else env
    config = dict(DEFAULTS)
    for key, default in DEFAULTS.items():
        value = env.get("APP_" + key.upper())
        if value is not None:
            config[key] = _convert(value, default)
    return config
