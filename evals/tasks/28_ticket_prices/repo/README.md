# Ticket booking

Prices are in cents.

| Kind   | Price |
|--------|-------|
| adult  | 1250  |
| child  | 600   |
| senior | 900   |

`total_cents(tickets, discount_percent=0)` takes a list of `(kind, quantity)`
pairs and returns the total price in cents.

The discount is a whole-number percent taken off the total. The discount
amount is rounded down to a whole cent.
