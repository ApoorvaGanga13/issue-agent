import os

from defaults import DEFAULTS


def load(env=None):
    env = os.environ if env is None else env
    config = DEFAULTS
    for key in config:
        value = env.get("APP_" + key.upper())
        if value is not None:
            config[key] = value
    return config
