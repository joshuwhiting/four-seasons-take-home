from pages.base_page import BasePage

# A single hotel/resort landing page: pick dates and check rates.
class PropertyPage(BasePage):

    def open_calendar(self):
        self.page.get_by_role("button", name="Selected Dates").click()
        self.page.get_by_role("application", name="Calendar Stay Dates").wait_for()

    def select_date(self, check_in: str, check_out: str, max_month_clicks : int = 6):
        self.open_calendar()
        self._click_calendar(check_in, max_month_clicks)
        self._click_calendar(check_out, max_month_clicks)


    def _click_calendar(self, target : str, max_month_clicks : int):
        date_button = self.page.get_by_role("button", name=target)
        clicks = 0
        while not date_button.is_visible() and clicks < max_month_clicks:
            self.page.get_by_role("button", name="Next Month").click()
            clicks += 1
        date_button.click()

    def check_rates(self):
        self.page.get_by_role("button", name="Check Rates", exact=True).click()
