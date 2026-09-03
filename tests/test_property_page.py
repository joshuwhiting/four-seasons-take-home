from pages.property_page import PropertyPage
from utils.date_helpers import get_future_date

PROPERTY_URL = "https://www.fourseasons.com/cabodelsol/"

def _calendar_label(d):
    # Matches the calendar day button aria-label, e.g. "September 20, 2026"
    return d.strftime("%B %-d, %Y")

def test_select_dates_and_check_rates(page):
    property_page = PropertyPage(page)
    property_page.goto(PROPERTY_URL)

    # Dismiss the cookie banner if it shows up so it doesn't cover the form.
    try:
        page.get_by_role("button", name="AGREE").click(timeout=5000)
    except Exception:
        pass

    check_in, check_out = get_future_date()
    property_page.select_date(_calendar_label(check_in), _calendar_label(check_out))
    property_page.check_rates()

    page.wait_for_url("**/accommodations/**")
    assert f"checkInDate={check_in.isoformat()}" in page.url
    assert f"checkOutDate={check_out.isoformat()}" in page.url
