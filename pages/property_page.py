from pages.base_page import BasePage
from utils.date_helpers import get_future_date, format_date_label


class CalendarDateUnavailable(Exception):
    """A requested check-in/check-out day isn't offered as a selectable date
    in the calendar. Callers can catch this to fall back to other dates."""


# A single hotel/resort landing page: pick dates and check rates.
class PropertyPage(BasePage):

    # Clicks "Selected Dates" to open the calendar widget and waits for it to render.
    def open_calendar(self):
        self.page.get_by_role("button", name="Selected Dates").click()
        self.page.get_by_role("application", name="Calendar Stay Dates").wait_for()

    # Opens the calendar and selects both check-in and check-out dates.
    # check_in = day user checks in
    # check_out = day user checks out
    # max_month_clicks = safety cap on how many times to click "Next month"
    def select_date(self, check_in: str, check_out: str, max_month_clicks: int = 5):
        self.open_calendar()
        self._click_calendar(check_in, max_month_clicks)
        self._click_calendar(check_out, max_month_clicks)

    # Tries days_from_now; if restricted or sold out, retries once a week later.
    def select_dates_with_retry(self, availability_page, days_from_now: int = 78, stay_length: int = 2):
        property_url = self.page.url
        for i, attempt_offset in enumerate((0, 7)):
            if i > 0:
                self.page.goto(property_url)
            checkin, checkout, nights = get_future_date(
                days_from_now=days_from_now + attempt_offset,
                stay_length=stay_length,
            )
            try:
                self.select_date(
                    format_date_label(checkin, "check-in"),
                    format_date_label(checkout, "check-out"),
                )
                self.check_rates()
            except CalendarDateUnavailable:
                continue  # this specific date wasn't selectable — try the next offset

            if availability_page.has_rooms_available():
                return nights
        raise AssertionError(
            f"No rooms available at {days_from_now} or {days_from_now + 7} days out"
        )

    # Pages forward through the calendar (clicking "Next month") until the
    # target date is present, visible, and enabled — then clicks it. Gives up
    # after max_month_clicks attempts, raising CalendarDateUnavailable if the
    # date never becomes selectable.
    def _click_calendar(self, target: str, max_month_clicks: int):
        date_button = self.page.get_by_role("button", name=target, exact=True)
        next_button = self.page.get_by_role("button", name="Next month")
        clicks = 0
        while not (date_button.count() and date_button.first.is_visible() and date_button.first.is_enabled()):
            if clicks >= max_month_clicks:
                raise CalendarDateUnavailable(f"Calendar day not selectable: {target}")
            next_button.click()
            self.page.wait_for_timeout(400)  # let the month transition settle
            clicks += 1
        date_button.first.click()

    # Click check rates button
    def check_rates(self):
        self.page.get_by_role("button", name="Check Rates", exact=True).first.click()
