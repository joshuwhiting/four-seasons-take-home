from pages.property_page import PropertyPage

class HotelSearchPage(PropertyPage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"
    
    def expand_region(self, region_name: str):
        button = self.page.get_by_role("button", name=region_name)
        if button.get_attribute("aria-expanded") == "false":
            button.click()

    def select_property(self, property_link_name: str):
        self.page.get_by_role("link", name=property_link_name).click()
