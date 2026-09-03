from pages.hotel_search_page import HotelSearchPage



def test_can_search_and_select_hotel(page):
    search_page = HotelSearchPage(page)
    search_page.goto(HotelSearchPage.URL)

    search_page.select_hotel(region_label="North America 55 properties", hotel_name="Los Cabos (Cabo Del Sol)")

    assert "cabo" in page.url.lower()
    page.get_by_role("navigation", name="Top Navigation").wait_for()