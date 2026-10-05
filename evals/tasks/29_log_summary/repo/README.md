# Log summary

Log lines look like this:

    2026-03-01 12:00:02 ERROR payments Card declined for order 17

The fields are date, time, level, service, and a message that can contain spaces.

`summarize(lines)` returns a dict that counts the lines for each level.

`error_rate(lines, service)` is the share of that service's own lines whose
level is ERROR, as a number from 0 to 1. It is 0.0 when the service has no lines.

Blank lines are ignored by both functions.
