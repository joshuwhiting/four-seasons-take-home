from datetime import date, timedelta

def get_future_date(days_from_now: int = 60, stay_length: int = 2):
    checkin = date.today() + timedelta(days=days_from_now)
    checkout = checkin + timedelta(days=stay_length)
    return checkin, checkout, stay_length

def format_date_label(target_date: date, prefix: str):
    # Matches the calendar day button aria-label, e.g.
    # "Available check-in date Friday, September 4, 2026"
    return target_date.strftime(f"Available {prefix} date %A, %B %-d, %Y")
