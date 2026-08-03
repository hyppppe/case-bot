import os

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# Публичный HTTPS-адрес, по которому будет открываться мини-апп.
# Telegram не открывает WebApp по http:// или localhost — нужен реальный
# HTTPS-домен (на проде) или туннель вроде ngrok (для локальной разработки).
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")

# На чём слушает aiohttp-сервер, который отдаёт мини-апп и API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", 8080))

# Игровые константы
START_BALANCE = 1000   # стартовый баланс нового игрока
SPIN_COST = 100         # цена одного открытия кейса
