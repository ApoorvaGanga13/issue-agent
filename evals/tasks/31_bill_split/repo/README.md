# Bill splitting

All amounts are whole cents.

`split_bill(total_cents, n)` splits a bill between `n` people. The shares add
up to the total exactly. When the total does not divide evenly, the first
shares are one cent larger than the rest. `n` must be at least 1, otherwise
ValueError is raised.

`with_tip(total_cents, tip_percent)` adds a tip. `tip_percent` is a whole
number. The tip is rounded to the nearest cent, and halves round up.

`per_person(total_cents, tip_percent, n)` adds the tip first, then splits.
