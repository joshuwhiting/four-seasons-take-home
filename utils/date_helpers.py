from datetime import date, timedelta

def get_future_date(days_from_now: int = 30, stay_length: int = 2):
    checkin = date.today() + timedelta(days=days_from_now)
    checkout = checkin + timedelta(days=stay_length)
    return checkin, checkout
