from pages.hotel_search_page import HotelSearchPage
from pages.property_page import PropertyPage
from pages.availability_page import AvailabilityPage
from pages.cart_page import CartPage

def test_search_select_dates_add_to_cart_and_verify(page):
    search_page = HotelSearchPage(page)
    property_page = PropertyPage(page)
    availability_page = AvailabilityPage(page)
    cart_page = CartPage(page)

    # 1. Navigate and select hotel
    search_page.goto(HotelSearchPage.URL)
    search_page.expand_region("North America")
    search_page.select_property("Los Cabos (Cabo Del Sol)")

    # 2. Select dates and check rates, retrying one week later if sold out
    nights = property_page.select_dates_with_retry(availability_page, days_from_now=30)

    # 3. Add a room to cart
    nightly_price = availability_page.get_first_room_nightly_price()
    availability_page.add_first_room_to_cart()

    # 4. Verify cart shows the room with pricing consistent with the selection
    cart_page.open_cart()
    assert cart_page.verify_room(), "No room line item visible in cart"

    expected_total = nightly_price * nights
    actual_total = cart_page.get_room_subtotal()

    # 5 Confirms the price is the expected price
    assert abs(actual_total - expected_total) < 1.00, (
        f"Cart subtotal {actual_total} doesn't match expected {expected_total} "
        f"({nightly_price} x {nights} nights)"
    )
