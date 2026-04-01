from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Transaction:
    id: str
    date: date
    amount: float
    merchant: str
    comment: str
    category: str


@dataclass(slots=True)
class BudgetLimit:
    category: str
    limit: float
