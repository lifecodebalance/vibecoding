from datetime import date

from finoptima.domain.models import BudgetLimit, Transaction
from finoptima.services.budget_control import budget_warnings, category_summary
from finoptima.services.categorizer import categorize_transaction


def test_categorize_transaction_products() -> None:
    assert categorize_transaction("Пятерочка", "") == "Продукты"


def test_budget_warning_for_food_limit() -> None:
    txs = [
        Transaction(
            id="1",
            date=date(2026, 3, 1),
            amount=2200,
            merchant="Кафе",
            comment="",
            category="Еда",
        ),
        Transaction(
            id="2",
            date=date(2026, 3, 2),
            amount=1200,
            merchant="Delivery",
            comment="",
            category="Еда",
        ),
    ]
    limits = [BudgetLimit(category="Еда", limit=3000)]

    summary = category_summary(txs)
    assert summary["Еда"] == 3400

    warnings = budget_warnings(txs, limits)
    assert len(warnings) == 1
    assert "Превышение лимита" in warnings[0]
