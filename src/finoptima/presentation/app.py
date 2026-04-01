from __future__ import annotations

import json
import uuid
from datetime import date
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for

from finoptima.domain.models import BudgetLimit, Transaction
from finoptima.services.budget_control import budget_warnings, category_summary, recommendation
from finoptima.services.categorizer import categorize_transaction

BASE_DIR = Path(__file__).resolve().parents[3]
LIMITS_FILE = BASE_DIR / "data" / "budget_limits.example.json"
TEST_DATA_FILE = BASE_DIR / "data" / "transactions.seed.json"


def load_limits() -> list[BudgetLimit]:
    raw = json.loads(LIMITS_FILE.read_text(encoding="utf-8"))
    return [BudgetLimit(category=item["category"], limit=float(item["limit"])) for item in raw]


def load_seed_transactions() -> list[Transaction]:
    raw = json.loads(TEST_DATA_FILE.read_text(encoding="utf-8"))
    result: list[Transaction] = []
    for item in raw:
        result.append(
            Transaction(
                id=item["id"],
                date=date.fromisoformat(item["date"]),
                amount=float(item["amount"]),
                merchant=item["merchant"],
                comment=item.get("comment", ""),
                category=item["category"],
            )
        )
    return result


app = Flask(__name__)
transactions: list[Transaction] = load_seed_transactions()
limits: list[BudgetLimit] = load_limits()


@app.post("/transactions")
def add_transaction():
    merchant = request.form["merchant"].strip()
    comment = request.form.get("comment", "").strip()
    amount = float(request.form["amount"])

    tx = Transaction(
        id=str(uuid.uuid4()),
        date=date.today(),
        amount=amount,
        merchant=merchant,
        comment=comment,
        category=categorize_transaction(merchant, comment),
    )
    transactions.append(tx)
    return redirect(url_for("index"))


@app.get("/")
def index():
    summary = category_summary(transactions)
    warnings = budget_warnings(transactions, limits)
    tip = recommendation(transactions, limits)

    return render_template_string(
        """
        <h1>FinOptima Lite</h1>

        <h2>Добавить транзакцию</h2>
        <form method="post" action="/transactions">
            <input name="merchant" placeholder="Магазин/мерчант" required>
            <input name="amount" type="number" min="0" step="0.01" placeholder="Сумма" required>
            <input name="comment" placeholder="Комментарий">
            <button type="submit">Добавить</button>
        </form>

        <h2>Список транзакций</h2>
        <ul>
            {% for tx in transactions %}
              <li>{{ tx.date }} | {{ tx.merchant }} | {{ '%.2f' % tx.amount }} | {{ tx.category }}</li>
            {% endfor %}
        </ul>

        <h2>Сводка по категориям</h2>
        <ul>
            {% for category, total in summary.items() %}
              <li>{{ category }}: {{ '%.2f' % total }}</li>
            {% endfor %}
        </ul>

        <h2>Предупреждения</h2>
        {% if warnings %}
            <ul>
            {% for w in warnings %}<li>{{ w }}</li>{% endfor %}
            </ul>
        {% else %}
            <p>Превышений нет.</p>
        {% endif %}

        <h2>Рекомендация</h2>
        <p>{{ tip }}</p>
        """,
        transactions=transactions,
        summary=summary,
        warnings=warnings,
        tip=tip,
    )


if __name__ == "__main__":
    app.run(debug=True)
