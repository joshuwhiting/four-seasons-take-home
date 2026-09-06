import re

_CAD_RE = re.compile(r"CAD\s*([\d,]+(?:\.\d+)?)")

def parse_cad_amount(text: str | None) -> float:
    # Pulls the numeric value out of a "CAD 2,397" / "CAD 4,794.07" string.
    match = _CAD_RE.search(text or "")
    assert match, f"No CAD amount found in: {text!r}"
    return float(match.group(1).replace(",", ""))
