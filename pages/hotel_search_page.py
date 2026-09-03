from pages.property_page import PropertyPage

class HotelSearchPage(PropertyPage):
    URL = "https://www.fourseasons.com/find_a_hotel_or_resort/"

    def select_hotel(self, region_label, hotel_name):
        region = self.page.get_by_role("region", name=region_label)

        # if page is smaller, or mobile layout, the dropdown hides the hotels/resorts
        if not region.is_visible():
            self.page.get_by_role("button", name=region_label).click()

        region.wait_for()
        region.get_by_text(hotel_name, exact=True).click()
            
        
