from pages.base_page import BasePage

# expand the region and search the hotel, then click the property 
class HotelSearchPage(BasePage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"

    # Expands the region's accordion toggle(s), if collapsed. The page repeats
    # the same region name across several property-type groupings, so there can
    # be multiple matching buttons — expand every collapsed one.
    def expand_region(self, region_name: str):
        buttons = self.page.get_by_role("button", name=region_name)
        visible_buttons = buttons.filter(visible=True)
        visible_buttons.first.wait_for()
        count = visible_buttons.count()
        for i in range(count):
            button = visible_buttons.nth(i)
            if button.get_attribute("aria-expanded") == "false":
                button.click()

    # Navigates to that property's page. Only expands the region accordion(s) if
    # the property link isn't already reachable, so a dropdown that's already
    # open is left untouched.
    def select_property(self, region_name: str, property_link_name: str):
        link = self.page.get_by_role("link", name=property_link_name).filter(visible=True).first
        if not link.is_visible():
            self.expand_region(region_name)
            link.wait_for(state="visible")
        link.click()
