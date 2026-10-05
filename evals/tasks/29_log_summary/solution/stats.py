from logparse import parse_line


def _entries(lines):
    return [parse_line(line) for line in lines if line.strip()]


def summarize(lines):
    counts = {}
    for entry in _entries(lines):
        counts[entry["level"]] = counts.get(entry["level"], 0) + 1
    return counts


def error_rate(lines, service):
    own = [e for e in _entries(lines) if e["service"] == service]
    if not own:
        return 0.0
    return sum(1 for e in own if e["level"] == "ERROR") / len(own)
