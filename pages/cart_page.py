import re
from pages.base_page import BasePage
from utils.price_helpers import parse_cad_amount


# booking cart
class CartPage(BasePage):

    # A private helper that returns a locator for the cart dialog itself
    @property
    def _panel(self):
        return self.page.get_by_role("dialog", name="User Panel")

    # Clicks the button that opens the cart panel
    def open_cart(self):
        # A cookie/privacy dialog can sit over the page on first load.
        agree = self.page.get_by_role("button", name="Agree")
        if agree.count() and agree.first.is_visible():
            agree.first.click()
        self.page.get_by_role("button", name="View cart").last.click()
        self._panel.wait_for(timeout=15000)

    def verify_room(self):
        # Each line item in the cart has a "Remove" control.
        return self._panel.get_by_role("button", name="Remove").first.is_visible()

    # The cart line item shows the stay subtotal (nightly rate x nights),
    # not the per-night price shown on the availability page.
    def get_room_subtotal(self):
        text = self._panel.get_by_text(re.compile(r"CAD\s+[\d,.]+")).first.text_content()
        return parse_cad_amount(text)
