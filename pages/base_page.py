from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

#  BasePage - __init__, goto
class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)
        self.dismiss_cookie_banner()

    # The cookie/privacy consent banner is injected a moment after load and can
    # sit over the page and gate session JS. Dismiss it once, up front.
    # timeout is generous after a fresh navigation (the banner loads late) and
    # short for opportunistic re-checks where the page is already settled.
    def dismiss_cookie_banner(self, timeout: int = 5000):
        agree = self.page.get_by_role("button", name="Agree")
        try:
            agree.first.wait_for(state="visible", timeout=timeout)
            agree.first.click()
        except PlaywrightTimeoutError:
            pass  # banner didn't show
