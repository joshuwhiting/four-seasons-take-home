from playwright.sync_api import Page


class PropertyPage:

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url : str):
        self.page.goto(url)