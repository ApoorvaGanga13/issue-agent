def parse_line(line):
    parts = line.strip().split(" ", 4)
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4],
    }
