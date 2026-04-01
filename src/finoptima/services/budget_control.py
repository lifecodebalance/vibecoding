from __future__ import annotations

from collections import defaultdict

from finoptima.domain.models import BudgetLimit, Transaction


def category_summary(transactions: list[Transaction]) -> dict[str, float]:
    summary: dict[str, float] = defaultdict(float)
    for tx in transactions:
        summary[tx.category] += tx.amount
    return dict(summary)


def budget_warnings(
    transactions: list[Transaction],
    limits: list[BudgetLimit],
) -> list[str]:
    summary = category_summary(transactions)
    warnings: list[str] = []

    for limit in limits:
        spent = summary.get(limit.category, 0.0)
        if spent > limit.limit:
            warnings.append(
                (
                    f"Превышение лимита в категории '{limit.category}': "
                    f"потрачено {spent:.2f}, лимит {limit.limit:.2f}."
                )
            )
    return warnings


def recommendation(transactions: list[Transaction], limits: list[BudgetLimit]) -> str:
    warnings = budget_warnings(transactions, limits)
    if not warnings:
        return "Лимиты не превышены. Продолжайте придерживаться текущего плана."

    return (
        "Рекомендация: сократите траты в категориях с превышением лимита, "
        "перенесите необязательные покупки на следующий месяц."
    )
