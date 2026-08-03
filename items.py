import random

# Содержимое кейса. weight — относительный шанс выпадения (сумма = 100,
# удобно читать как проценты). value — сколько монет зачисляется игроку.
# Можно менять баланс value/weight, чтобы регулировать отдачу кейса (RTP).
ITEMS = [
    {"name": "Обычный болтик",     "value": 10,   "weight": 45, "rarity": "common"},
    {"name": "Стальной ключ",      "value": 25,   "weight": 25, "rarity": "uncommon"},
    {"name": "Серебряный жетон",   "value": 60,   "weight": 15, "rarity": "rare"},
    {"name": "Золотая монета",     "value": 150,  "weight": 8,  "rarity": "epic"},
    {"name": "Бриллиант",          "value": 400,  "weight": 5,  "rarity": "legendary"},
    {"name": "Мифический артефакт","value": 1500, "weight": 2,  "rarity": "mythic"},
]


def roll_item() -> dict:
    """Взвешенный случайный выбор предмета. Вызывается ТОЛЬКО на сервере —
    клиенту нельзя доверять результат."""
    weights = [item["weight"] for item in ITEMS]
    return random.choices(ITEMS, weights=weights, k=1)[0]
