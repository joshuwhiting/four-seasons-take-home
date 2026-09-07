from pages.base_page import BasePage
from utils.price_helpers import PRICE_RE, parse_cad_amount


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

    def verify_room(self) -> bool:
        try:
            self._panel.get_by_role("button", name="Remove").first.wait_for(timeout=10000)
            return True
        except Exception:
            return False
        
    # The cart line item shows the stay subtotal (nightly rate x nights),
    # not the per-night price shown on the availability page.
    def get_room_subtotal(self):
        text = self._panel.get_by_text(PRICE_RE).first.text_content()
        assert text is not None, "Could not find a price in the cart panel"
        return parse_cad_amount(text)
