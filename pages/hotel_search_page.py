from pages.base_page import BasePage

# expand the region and search the hotel, then click the proptery 
class HotelSearchPage(BasePage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"

    def expand_region(self, region_name: str):
        button = self.page.get_by_role("button", name=region_name)
        if button.get_attribute("aria-expanded") == "false":
            button.click()

    def select_property(self, property_link_name: str):
        self.page.get_by_role("link", name=property_link_name).click()
