# Arbitrage Trading Bot

A lightweight Python service that monitors Polymarket markets for BTC mispricings and sends email alerts when an arbitrage opportunity is detected.

---

## Architecture
*Data ingestion → P&L calculation → Alert dispatch*

---

## Features
<img width="1898" height="1018" alt="image" src="https://github.com/user-attachments/assets/12b299fd-6891-466d-a5e0-20351f455b63" />
<img width="1487" height="787" alt="image" src="https://github.com/user-attachments/assets/f4a4c5b8-2caf-4b11-9ea7-bd3b532a997f" />



- **Real-time scanning** of BTC markets on Polymarket  
- **Automated P/L computation** across multiple strike thresholds  
- **Email notifications** with throttling (once per market every 8 hrs)  
- **Secure credentials** stored via Fernet encryption  

---

## Quickstart

```bash
git clone git@github.com:henrywei8/trading-bot.git
cd trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Encrypt your email and add key to SECRETS_KEY
python encrypt_email.py youremail@example.com > encrypted.txt

# Run the bot
python main.py
