import random

# Содержимое кейса. weight измеряется в сотых долях процента (базисных
# пунктах / 100), т.е. 4500 = 45.00%. Так можно точно задать джекпоту шанс
# 0.01%, оставаясь в целых числах. value — сколько монет зачисляется игроку.
ITEMS = [
    {"name": "Обычный болтик",     "value": 10,    "weight": 4500, "rarity": "common"},
    {"name": "Стальной ключ",      "value": 25,    "weight": 2500, "rarity": "uncommon"},
    {"name": "Серебряный жетон",   "value": 60,    "weight": 1500, "rarity": "rare"},
    {"name": "Золотая монета",     "value": 150,   "weight": 800,  "rarity": "epic"},
    {"name": "Бриллиант",          "value": 400,   "weight": 500,  "rarity": "legendary"},
    {"name": "Мифический артефакт","value": 1500,  "weight": 200,  "rarity": "mythic"},
    {"name": "Джекпот",            "value": 50000, "weight": 1,    "rarity": "jackpot"},  # 0.01%
]


def roll_item() -> dict:
    """Взвешенный случайный выбор предмета. Вызывается ТОЛЬКО на сервере —
    клиенту нельзя доверять результат."""
    weights = [item["weight"] for item in ITEMS]
    return random.choices(ITEMS, weights=weights, k=1)[0]
