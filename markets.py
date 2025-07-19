import re
import json
import requests

POLY_URL = "https://gamma-api.polymarket.com/events"
DOLLAR_RE = re.compile(r"\$(?P<num>[\d,]+)(?P<suffix>[Kk]?)")

def btc_price():
    resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "usd"}
    )
    resp.raise_for_status()
    return resp.json()["bitcoin"]["usd"]

def fetch_all_events(limit=100):
    offset = 0
    while True:
        resp = requests.get(POLY_URL, params={
            "closed": "false", "limit": limit, "offset": offset
        })
        resp.raise_for_status()
        page = resp.json()
        if not page:
            break
        yield from page
        offset += limit

def parse_target_price(text: str) -> int | None:
    m = DOLLAR_RE.search(text)
    if not m:
        return None
    num = int(m.group("num").replace(",", ""))
    if m.group("suffix").lower() == "k":
        num *= 1_000
    return num

def safe_parse_prices(raw):
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, str):
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            return None
    else:
        return None

    try:
        return [float(p) for p in items]
    except (TypeError, ValueError):
        return None

def extract_markets(min_no_price: float = 0.95,
                    verbs: str = r"\b(hit|pass|reach|above|greater than|close above)\b"
                   ) -> list[tuple[str, float, int]]:
    current = btc_price()
    out = []

    for ev in fetch_all_events(limit=100):
        title = ev.get("title", "")
        if "bitcoin" not in title.lower():
            continue

        for opt in ev.get("markets", []):
            q = opt.get("question", "")
            if not re.search(verbs, q, re.I):
                continue

            strike = parse_target_price(q)
            if strike is None or strike <= current:
                continue

            prices = safe_parse_prices(opt.get("outcomePrices"))
            if not prices or len(prices) < 2:
                continue

            no_price = prices[1]
            if no_price > min_no_price:
                continue

            cond_id = opt.get("conditionId")
            out.append((cond_id, no_price, strike))

    return out


if __name__ == "__main__":
    for cond_id, no_price, strike in extract_markets():
        print(cond_id, no_price, strike)
