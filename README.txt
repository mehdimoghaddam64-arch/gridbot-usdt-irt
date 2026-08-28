GRID BOT - USDT/IRT

Current mode: PAPER TRADING ONLY.
No real orders are sent to Wallex.

Render deployment:
1. Upload project to GitHub.
2. Render -> New -> Web Service.
3. Connect repository.
4. Build: pip install -r requirements.txt
5. Start: gunicorn --bind 0.0.0.0:$PORT app:app
6. Free plan -> Deploy.

Never put a Wallex API key in frontend code or GitHub.
