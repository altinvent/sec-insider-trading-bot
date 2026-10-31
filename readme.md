\# Real-Time SEC Form 4 Insider Trading Bot 📈



A lightweight Python starter bot that tracks open-market executive stock purchases and sales (SEC Form 4 filings) for public US equities (like `TSLA`, `NVDA`, `AAPL`) and dispatches real-time alerts to Discord or terminal consoles.



Powered by the \*\*\[SEC Form 4 Insider Trades API on RapidAPI](https://rapidapi.com/altinvent-altinvent-default/api/sec-form-4-insider-trades-api)\*\*.



\---



\## Features

\- \*\*Real-Time Data:\*\* Queries official SEC EDGAR Form 4 filings parsed into clean JSON.

\- \*\*Value Filters:\*\* Screen out insignificant stock grants and micro-allocations (e.g., alert only on trades > $100k).

\- \*\*Discord Integration:\*\* Sends color-coded Discord webhook embeds (Green = Buy, Red = Sell).

\- \*\*Free to Start:\*\* Includes 50 free API requests per month on RapidAPI.



\---



\## Quickstart



\### 1. Clone the repository

```bash

git clone \[https://github.com/](https://github.com/)<YOUR\_GITHUB\_USERNAME>/sec-insider-trading-bot.git

cd sec-insider-trading-bot

