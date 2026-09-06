from pages.base_page import BasePage

# A single hotel/resort landing page: pick dates and check rates.
class PropertyPage(BasePage):

    # opens the calendar
    def open_calendar(self):
        self.page.get_by_role("button", name="Selected Dates").click()
        self.page.get_by_role("application", name="Calendar Stay Dates").wait_for()

    # select the date
    def select_date(self, check_in: str, check_out: str, max_month_clicks: int = 12):
        self.open_calendar()
        self._click_calendar(check_in, max_month_clicks)
        self._click_calendar(check_out, max_month_clicks)

    def _click_calendar(self, target: str, max_month_clicks: int):
        # The calendar shows two months at a time; page forward until the target day is rendered, then click it.
        date_button = self.page.get_by_role("button", name=target, exact=True)
        next_button = self.page.get_by_role("button", name="Next month")
        clicks = 0
        while not (date_button.count() and date_button.first.is_visible()):
            if clicks >= max_month_clicks:
                raise AssertionError(f"Calendar day not found: {target}")
            next_button.click()
            self.page.wait_for_timeout(400)  # let the month transition settle
            clicks += 1
        date_button.first.click()

    def check_rates(self):
        self.page.get_by_role("button", name="Check Rates", exact=True).first.click()
