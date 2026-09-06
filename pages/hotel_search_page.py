from pages.base_page import BasePage

# expand the region and search the hotel, then click the proptery 
class HotelSearchPage(BasePage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"

    # Expands the region's accordion toggle, if it's collapsed.
    def expand_region(self, region_name: str):
        buttons = self.page.get_by_role("button", name=region_name)
        visible_button = buttons.filter(visible=True)
        visible_button.wait_for()
        if visible_button.get_attribute("aria-expanded") == "false":
            visible_button.click()

    # Nagviates to that proptery's page.
    def select_property(self, property_link_name: str):
        self.page.get_by_role("link", name=property_link_name).click()
