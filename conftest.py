import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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