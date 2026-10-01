from calendar_utils import days_in_month

def test_leap_years():
    assert days_in_month(2024, 2) == 29
    assert days_in_month(2000, 2) == 29

def test_century_not_leap():
    assert days_in_month(1900, 2) == 28

def test_other_months():
    assert days_in_month(2023, 2) == 28
    assert days_in_month(2023, 4) == 30
    assert days_in_month(2023, 1) == 31
