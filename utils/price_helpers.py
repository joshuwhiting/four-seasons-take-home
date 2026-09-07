import re

# Matches a displayed price for any 3-letter currency code (USD, CAD, MXN, ...),
# e.g. "USD 1,234" or "CAD 4,794.07". Shared by the page objects for both
# locating price text and parsing the number out of it.
PRICE_RE = re.compile(r"[A-Z]{3}\s+([\d,]+(?:\.\d+)?)")


def parse_price_amount(text: str | None):
    match = PRICE_RE.search(text or "")
    assert match is not None, f"Could not parse an amount from: {text!r}"
    return float(match.group(1).replace(",", ""))
