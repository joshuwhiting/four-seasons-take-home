from playwright.sync_api import Page

#  BasePage - __init__, goto
class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)
