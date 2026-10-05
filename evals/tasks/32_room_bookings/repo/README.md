# Room bookings

A booking is a pair `(start, end)` of day numbers. It occupies the nights from
`start` up to, but not including, `end`. A booking that starts on the day
another one ends does not overlap it.

- `overlaps(a, b)` says whether two bookings share a night.
- `can_book(existing, new)` is True when `new` overlaps none of the existing bookings.
- `overlaps` and `can_book` raise ValueError for a booking that does not end after it starts.
- `nights(booking)` is the number of nights it occupies.
- `total_nights(bookings)` adds up the nights of all bookings.
