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

- Page Object Model. One class per screen (`HotelSearchPage`, `PropertyPage`,
  `AvailabilityPage`, `CartPage`), each extending a thin `BasePage` that owns the
  `page` handle and `goto()`. The test reads as a sequence of intent, not selectors.
- Pure logic split into `utils/`. `date_helpers.py` (date math, calendar aria
  labels) and `price_helpers.py` (`"CAD #,###"` -> float) have no Playwright
  dependency, so they're trivial to reason about and reuse.

### Locator strategy

- Prefer accessible roles and names (`get_by_role("button", name=...)`) as the default.
- Fall back to `data-tracking-id` when visible text is unstable — e.g.
  `[data-tracking-id="add-to-cart"]`, which also naturally excludes rooms that only
  offer "Select Bed Options".

### Resilience against a live site

- Dates are computed at runtime, never hardcoded, so the test doesn't rot.
- Retry logic at two levels: `select_dates_with_retry()` retries a week later
  when the target dates are restricted or sold out; `_click_calendar()` pages
  forward month by month with a `max_month_clicks` safety cap and raises a custom
  `CalendarDateUnavailable` for clean fallback control flow.
- Interstitials handled explicitly: cookie/privacy dialog, the post-add upsell
  page, and the header control flipping to "view cart".
- Explicit `wait_for()` on meaningful elements rather than fixed sleeps for
  synchronization. (The one `wait_for_timeout` in the test is a deliberate pause
  to hold the final cart view on screen for the video recording, not a sync wait.)

### Verification approach

- Price is checked by math: capture the nightly rate on the availability page,
  multiply by the number of nights, and compare to the cart subtotal with a
  $1.00 tolerance to absorb rounding.

### Test ergonomics

- Runs headed by default so the flow is watchable; `HEADLESS=1` for CI.
- Video recording and function-scoped fixtures for per-test isolation
  (`conftest.py`).

## CI/CD

See `.github/workflows/test.yml` for a GitHub Actions example that would
run this suite daily on a cron schedule or on demand via
workflow_dispatch. It installs dependencies, installs Playwright
browsers and runs pytest.
