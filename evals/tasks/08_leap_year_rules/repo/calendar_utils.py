def days_in_month(year, month):
    if month == 2:
        return 29 if year % 4 == 0 else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31
