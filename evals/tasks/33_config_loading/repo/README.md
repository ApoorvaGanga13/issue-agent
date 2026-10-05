# Config loading

`load(env=None)` returns the settings as a dict. `env` is a dict of environment
variables and defaults to `os.environ`.

- The defaults live in `defaults.py`.
- A setting called `port` is overridden by the variable `APP_PORT`, and so on.
- The value is converted to the type of the default. Integers use `int()`.
  For booleans, `true`, `1` and `yes` (any capital letters, spaces ignored)
  mean True and any other value means False.
- Variables that do not match a setting are ignored.
- An integer setting with a value that is not a number raises ValueError.
- The defaults are never modified, and every call returns a new dict.
