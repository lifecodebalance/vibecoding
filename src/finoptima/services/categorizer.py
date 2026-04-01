from __future__ import annotations

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Продукты": ("пятерочка", "перекресток", "магнит", "лента", "ашан"),
    "Транспорт": ("метро", "такси", "яндекс go", "автобус", "трамвай"),
    "Развлечения": ("кино", "театр", "netflix", "steam", "концерт"),
    "Еда": ("кафе", "ресторан", "доставка", "самокат", "delivery"),
    "Здоровье": ("аптека", "клиника", "стоматология"),
}


def categorize_transaction(merchant: str, comment: str = "") -> str:
    text = f"{merchant} {comment}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Другое"
