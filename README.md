# FinOptima Lite

Учебный MVP для лабораторной №6.

Цель: показать прототип финансового сервиса, созданного с помощью vibe-coding/Codex, и затем проанализировать его качество.

Функции MVP:
- добавить транзакцию
- автоматически определить категорию по ключевым словам
- показать список транзакций
- показать сумму расходов по категориям
- показать предупреждение о превышении бюджета
- вывести простую текстовую рекомендацию

Не нужно:
- авторизация
- настоящие банковские API
- настоящие инвестиционные операции
- production-безопасность

## Структура проекта

- `src/finoptima/domain` — доменная модель (`Transaction`, `BudgetLimit`)
- `src/finoptima/services/categorizer.py` — логика категоризации по ключевым словам
- `src/finoptima/services/budget_control.py` — сводка, предупреждения, рекомендация
- `src/finoptima/presentation/app.py` — web-представление (форма + список + отчёты)
- `data/budget_limits.example.json` — пример конфигурации лимитов бюджета
- `data/transactions.seed.json` — тестовые данные

## Как запустить

1. Перейдите в корень проекта:
   ```bash
   cd /workspace/vibecoding
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите тесты:
   ```bash
   pytest
   ```
5. Запустите приложение:
   ```bash
   PYTHONPATH=src flask --app finoptima.presentation.app run --debug
   ```
6. Откройте в браузере:
   ```
   http://127.0.0.1:5000
   ```
