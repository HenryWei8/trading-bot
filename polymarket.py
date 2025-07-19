import time
import requests
import os
from cryptography.fernet import Fernet
from py_clob_client.client import ClobClient
from markets import extract_markets, btc_price
from gmail import send_email

RECIPIENT = b"gAAAAABodCYgyy_W7SiEIt0AiA87-Fyuqd2Xo3fg6q4hBdGLiiLbQtVjGu_0m_fnBvvyr3fWFGHmszzGuD-VaGD0ReMSsarIkGEC0mHPOEEpE6HO1lH4YEI="
key = "PihHVFK7rzYDT-T5wrW_jElSCXhGFnGmq88b2Om7_hI="
if not key:
    raise RuntimeError("Missing SECRETS_KEY environment variable")

f = Fernet(key.encode())
raw = f.decrypt(RECIPIENT).decode()
EMAIL_RECIPIENT = raw.strip()

HOST     = "https://clob.polymarket.com"
CHAIN_ID = 137
client   = ClobClient(HOST, chain_id=CHAIN_ID)

PRINCIPAL       = 1000
POLL_INTERVAL   = 1000

# track last alert times
last_alert = {}              
ALERT_INTERVAL = 8 * 3600     # 8 hours

def run_scan():
    BTC = btc_price()
    triples = extract_markets(min_no_price=0.95)

    for condition_id, NO_PRICE, STRIKE in triples:
        market = client.get_market(condition_id=condition_id)
        if NO_PRICE == 0:
            continue
        slug   = market.get("market_slug") or condition_id

        for i in range(97, 0, -1):
            bottom = ((BTC - 30000) // 1000) * 1000
            top    = STRIKE

            OTM = PRINCIPAL * ((i/100) * (bottom / BTC)
                              + (1 - i/100) * (1 / NO_PRICE)) - PRINCIPAL
            ITM = PRINCIPAL * (i/100) * (top / BTC) - PRINCIPAL

            if OTM > -20 and ITM > 60:
                now = time.time()
                # skip if alerted this market within the interval
                if slug in last_alert and now - last_alert[slug] < ALERT_INTERVAL:
                    break

                link = f"https://polymarket.com/market/{slug}"
                msg = (
                    f"Arbitrage alert!\n\n"
                    f"Market: {slug}\n"
                    f"i = {i}%\n"
                    f"OTM P/L: {OTM:.2f}\n"
                    f"ITM P/L: {ITM:.2f}\n"
                    f"Link: {link}\n"
                    f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                print(msg)
                send_email(
                    EMAIL_RECIPIENT,
                    subject=f"[ARB SPOTTED] {slug} @ {i}%",
                    body=msg
                )
                last_alert[slug] = now

                if OTM > -10 and ITM > 100:
                    print("PERFECT ARB SPOTTED")
                    send_email(
                        EMAIL_RECIPIENT,
                        subject=f"[PERFECT ARB] {slug} @ {i}%",
                        body=msg + "\n\n*** PERFECT ARBITRAGE ***"
                    )
                break

if __name__ == "__main__":
    from gmail import get_gmail_service
    print("Authenticating with Gmail…")
    get_gmail_service()

    print("Starting polling loop every", POLL_INTERVAL, "seconds.")
    try:
        while True:
            run_scan()
            print("Current Iteration Ended")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by user.")
