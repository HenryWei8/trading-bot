# Arbitrage Trading Bot

A lightweight Python service that monitors Polymarket markets for BTC mispricings and sends email alerts when an arbitrage opportunity is detected.

---

## ⚙️ Architecture

![Pipeline Diagram](assets/architecture-diagram.png)  
*Data ingestion → P&L calculation → Alert dispatch*

---

## 🚀 Features

- **Real-time scanning** of BTC markets on Polymarket  
- **Automated P/L computation** across multiple strike thresholds  
- **Email notifications** with throttling (once per market every 8 hrs)  
- **Secure credentials** stored via Fernet encryption  

---

## 🔧 Quickstart

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
