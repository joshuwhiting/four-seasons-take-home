from pages.base_page import BasePage

# expand the region and search the hotel, then click the property 
class HotelSearchPage(BasePage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"

    # Expands the region's accordion toggle(s), if collapsed. The page repeats
    # the same region name across several property-type groupings, so there can
    # be multiple matching buttons — expand every collapsed one.
    def expand_region(self, region_name: str):
        buttons = self.page.get_by_role("button", name=region_name)
        visible_button = buttons.filter(visible=True)
        visible_button.wait_for()
        if visible_button.get_attribute("aria-expanded") == "false":
            visible_button.click()

    # Navigates to that property's page.
    def select_property(self, property_link_name: str):
        self.page.get_by_role("link", name=property_link_name).filter(visible=True).first.click()
