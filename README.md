# Solana Wallet Alert Bot

Deploy on Render as a worker service.

## Setup
- Add env vars on Render
- Push to GitHub
- Deploy worker

## Env vars
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` — where alerts get sent
- `HELIUS_API_KEY` — used to poll the watched wallet's transactions
- `WATCH_WALLET` — the Solana address to monitor
- `MARKETCAP_LIMIT` — only alert on tokens at or below this USD market cap
- `MIN_LIQUIDITY` — only alert on tokens at or above this USD liquidity
- `POLL_INTERVAL` — seconds between polls

## Filtering behavior
When a new transaction moves an SPL token, the bot looks up that token's
liquidity and market cap via DexScreener. The alert is only sent if the
token's market cap is **at or below** `MARKETCAP_LIMIT` and its liquidity is
**at or above** `MIN_LIQUIDITY`. This is meant to surface early/low-cap token
activity while filtering out tokens with too little liquidity to trust the
price data (e.g. likely rugs or empty pools). Transactions that don't involve
an SPL token (plain SOL transfers) are always alerted with no filtering, and
tokens DexScreener has no data for are skipped rather than alerted blindly.
