from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from utils.price_helpers import PRICE_RE, parse_price_amount

# Room results for the selected property and dates.
class AvailabilityPage(BasePage):

    # private function to find "Add to Cart" buttons, also naturally excludes rooms that
    # only show "Select Bed Options" instead)
    def _add_to_cart_buttons(self):
        return self.page.locator('[data-tracking-id="add-to-cart"]')

    # the first room card that actually has an "Add to Cart" button
    def _first_available_room_card(self):
        return self.page.locator(".FilteredColumnsList-item").filter(
            has=self._add_to_cart_buttons()
        ).first

    # verify if options are available
    def has_rooms_available(self):
        # wait for the results area to settle — either real rooms or bed-option rooms.
        # If neither ever renders the property is sold out for these dates.
        try:
            self.page.locator(
                '[data-tracking-id="add-to-cart"], button:has-text("Select Bed Options")'
            ).first.wait_for(timeout=40000)
        except PlaywrightTimeoutError:
            return False
        add_to_cart_visible = self._add_to_cart_buttons().first.is_visible()
        bed_options_visible = self.page.get_by_role("button", name="Select Bed Options").first.is_visible()
        return add_to_cart_visible or bed_options_visible

    # the "Avg. price per night" shown on the first available room card, as a number
    def get_first_room_nightly_price(self):
        room_card = self._first_available_room_card()
        price = room_card.get_by_text(PRICE_RE).first.text_content()
        return parse_price_amount(price)

    def add_first_room_to_cart(self):
        room_card = self._first_available_room_card()
        button = room_card.locator('[data-tracking-id="add-to-cart"]').first
        button.scroll_into_view_if_needed()
        button.click()
        self.page.wait_for_url("**/discover/**", timeout=30000)