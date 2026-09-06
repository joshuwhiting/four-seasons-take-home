import os
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def context():
    # Runs headed by default so the flow is visible. Set HEADLESS=1 to run
    # without a browser window (e.g. in CI).
    headless = os.environ.get("HEADLESS", "").lower() in ("1", "true", "yes")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        ctx = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 800},
        )
        yield ctx
        ctx.close()
        browser.close()

@pytest.fixture(scope="function")
def page(context):
    return context.new_page()
