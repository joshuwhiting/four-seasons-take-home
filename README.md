# Four Seasons Booking Flow — Test Automation

Automated end-to-end test for the Four Seasons hotel booking flow, built with
**Python + Playwright + pytest**, using the Page Object Model (POM).

## What it tests

Following the assessment's required flow:

1. Navigate to `fourseasons.com/find_a_hotel_or_resort/`
2. Select a Hotel (Cabo Del Sol)
3. Pick check-in/check-out dates with retry logic
4. Check rates for those dates
5. Add a room to the cart
6. Open the cart and verify the room is present, with pricing that matches

## Test Recording

![Test run](Recording/test_recording.gif)

Full-quality screen recording: [test_recording.webm](Recording/test_recording.webm)

## Project structure

```
four-seasons-take-home/
├── pages/
│   ├── base_page.py            # BasePage — shared __init__, goto(), cookie banner
│   ├── hotel_search_page.py    # region expand + property selection
│   ├── property_page.py        # calendar / date picking, "Check Rates"
│   ├── availability_page.py    # room list, price capture, "Add to Cart"
│   └── cart_page.py            # cart panel, room + price verification
├── utils/
│   ├── date_helpers.py         # computes a future date range dynamically
│   └── price_helpers.py        # parses "CAD #,###"-style strings to floats
├── tests/
│   └── test_book_room.py       # the end-to-end test
├── Recording/
│   ├── test_recording.gif
│   └── test_recording.webm
├── conftest.py                 # browser/context/page fixtures, video recording
├── .github/workflows/test.yml  # CI/CD
├── pytest.ini                  # pytest config (testpaths, etc.)
├── requirements.txt
└── README.md
```

## Running the tests

```bash
pip install -r requirements.txt
playwright install
pytest tests/test_book_room.py
```

## Design

### Architecture

I went with Page Object Model — one class per screen (`HotelSearchPage`, `PropertyPage`, `AvailabilityPage`, `CartPage`), each extending a thin `BasePage` that just holds the `page` handle and a `goto()` method. Point of this is so the test itself reads like a series of steps, not a pile of selectors.

Anything that's pure logic lives in `utils/` instead. `date_helpers.py` handles date math and calendar aria labels, `price_helpers.py` converts strings like `"CAD #,###"` into floats. Neither one touches Playwright, so they're easy to test or reuse on their own.

### Locator strategy

Default is accessible roles and names (`get_by_role("button", name=...)`). When the visible text isn't reliable, I fall back to `data-tracking-id` — e.g. `[data-tracking-id="add-to-cart"]`, which also happens to skip rooms that only offer "Select Bed Options" instead of a real add-to-cart button.

### Resilience against a live site

- Dates are calculated at runtime instead of hardcoded, so the test won't quietly break in a few months.
- Two layers of retry: `select_dates_with_retry()` tries a week later if the original dates are blocked or sold out, and `_click_calendar()` pages forward month by month (capped at `max_month_clicks`) before giving up and raising a `CalendarDateUnavailable`.
- Handled the interstitials directly — the cookie/privacy dialog, the upsell page that shows up after adding a room, and the header switching over to "view cart".
- Using `wait_for()` on actual elements instead of sleeping for a fixed amount of time. There's one `wait_for_timeout` in the test, but that's just to hold the cart view on screen long enough for the recording — not doing any synchronization work.

### Verification approach

Price gets checked with actual math: grab the nightly rate off the availability page, multiply by the number of nights, and compare that to the cart subtotal (with a $1 tolerance for rounding).

### Test ergonomics

Runs headed by default so you can actually watch it work — set `HEADLESS=1` for CI. Recording and function-scoped fixtures are set up in `conftest.py` so each test run stays isolated.

## CI/CD

`.github/workflows/test.yml` has a GitHub Actions example — installs dependencies and Playwright browsers, then runs pytest. Could run it daily on a cron or trigger it manually via workflow_dispatch.
