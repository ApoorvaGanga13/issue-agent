from logparse import parse_line


def summarize(lines):
    counts = {}
    for line in lines:
        entry = parse_line(line)
        counts[entry["level"]] = counts.get(entry["level"], 0) + 1
    return counts


def error_rate(lines, service):
    entries = [parse_line(line) for line in lines]
    errors = [e for e in entries if e["level"] == "ERROR" and e["service"] == service]
    return len(errors) / len(entries)
