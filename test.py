from markets import btc_price
PRINCIPAL = 1000
BTC = btc_price()
STRIKE = 150000
NO_PRICE = 0.57
i = 0.83
OUTCOMES = list(range(((BTC - 30000) // 1000) * 1000, STRIKE + 1000, 1000))
returns = []

for j in range(len(OUTCOMES)):
    price = OUTCOMES[j]
    if j != len(OUTCOMES) - 1:
        OTM = PRINCIPAL * (i*(price/BTC) + (1-i)/NO_PRICE) - PRINCIPAL
        returns.append(f"{price}:{round(OTM, 2)}")
    else:
        ITM = PRINCIPAL *i*(price/BTC) - PRINCIPAL
        returns.append(f"{price}:{round(ITM, 2)}")
print(returns)

# Market URL: https://polymarket.com/market/will-bitcoin-reach-150000-by-december-31-2025 — best i = 80%
# Market URL: https://polymarket.com/market/will-bitcoin-reach-130000-by-december-31-2025 — best i = 91%