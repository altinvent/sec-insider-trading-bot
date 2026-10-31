import os
import requests
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Target stocks to track
WATCHLIST = ["TSLA", "NVDA", "AAPL", "MSFT"]
MIN_TRADE_VALUE = 100000  # Ignore noise trades under $100k

def fetch_insider_trades(ticker: str, min_val: int = 100000):
    """Fetch structured Form 4 transactions from RapidAPI."""
    url = f"https://{RAPIDAPI_HOST}/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "ticker": ticker,
        "min_value": str(min_val),
        "limit": "5"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching data for {ticker}: {e}")
        return None

def send_discord_alert(trade: dict, company: str, ticker: str):
    """Format and dispatch a rich Discord Embed alert."""
    action = trade.get("action", "UNKNOWN")
    total_val = trade.get("total_value", 0)
    shares = trade.get("shares", 0)
    price = trade.get("price_per_share", 0)
    insider = trade.get("insider", "Unknown")
    title = trade.get("title", "Insider")
    trade_date = trade.get("trade_date", "N/A")

    # Visual cue: Green for Buy, Red for Sell, Blue for Award/Option
    if action == "BUY":
        color = 0x2ECC71  # Green
        action_emoji = "🟢 **BUY**"
    elif action == "SELL":
        color = 0xE74C3C  # Red
        action_emoji = "🔴 **SELL**"
    else:
        color = 0x3498DB  # Blue
        action_emoji = f"ℹ️ **{action}**"

    embed = {
        "title": f"🚨 Insider Alert: {ticker} ({company})",
        "description": f"{action_emoji} detected on SEC Form 4 filing.",
        "color": color,
        "fields": [
            {"name": "Executive / Insider", "value": f"**{insider}**\n*{title}*", "inline": True},
            {"name": "Total Value", "value": f"**${total_val:,.2f}**", "inline": True},
            {"name": "Details", "value": f"{shares:,.0f} shares @ ${price:,.2f}", "inline": True},
            {"name": "Trade Date", "value": trade_date, "inline": True},
            {"name": "Remaining Stack", "value": f"{trade.get('shares_held_after', 0):,.0f} shares", "inline": True}
        ],
        "footer": {"text": "Powered by SEC Form 4 Insider Trades API on RapidAPI"}
    }

    payload = {"embeds": [embed]}

    if DISCORD_WEBHOOK_URL:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if res.status_code in [200, 204]:
            print(f"[+] Alert sent to Discord for {ticker}: {insider} ({action})")
        else:
            print(f"[-] Discord delivery failed: HTTP {res.status_code}")
    else:
        # Fallback to console print if no webhook is supplied
        print(f"\n--- [ALERT] {ticker} ({action}) ---")
        print(f"Insider: {insider} ({title})")
        print(f"Volume:  {shares:,.0f} shares @ ${price:,.2f} (${total_val:,.2f})")
        print(f"Date:    {trade_date}\n")

def main():
    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        print("[!] Missing RAPIDAPI_KEY or RAPIDAPI_HOST in .env file.")
        return

    print("[*] Checking SEC Form 4 insider transactions across watchlist...")
    for ticker in WATCHLIST:
        data = fetch_insider_trades(ticker, min_val=MIN_TRADE_VALUE)
        if not data or "transactions" not in data:
            continue

        company = data.get("company", ticker)
        transactions = data.get("transactions", [])

        if not transactions:
            print(f"[*] No recent transactions over ${MIN_TRADE_VALUE:,} found for {ticker}.")
            continue

        for trade in transactions:
            send_discord_alert(trade, company, ticker)

if __name__ == "__main__":
    main()