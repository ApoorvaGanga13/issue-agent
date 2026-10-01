def merge(defaults, overrides):
    result = defaults
    for key, value in overrides.items():
        result[key] = value
    return result
