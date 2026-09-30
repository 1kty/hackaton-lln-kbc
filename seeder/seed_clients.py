"""Generate synthetic customer profiles with transactions for the KBC personalization hackathon."""

from __future__ import annotations

import argparse
import json
import random
import sqlite3
from pathlib import Path
from typing import Any


CATEGORIES = ["mobility", "groceries", "bars_restaurants", "other"]

MERCHANT_NAMES: dict[str, list[str]] = {
    "mobility": [
        "Shell", "Texaco", "Lukoy", "Q8", "BikeHub", "De Lijn",
        "SNCB", "Uber", "Dott", "Voi", "Cambio", "Parko",
    ],
    "groceries": [
        "Carrefour", "Delhaize", "Colruyt", "Aldi", "Lidl",
        "Bio-Planet", "OKay", "Cru", "Färm", "Proxy",
    ],
    "bars_restaurants": [
        "Le Pain Quotidien", "Exki", "Bocca", "Café Central",
        "La Belle Vie", "Bistro L", "Sushi Bar", "Pizza Hut",
        "Friterie", "Café Belga", "Restaurant Yuzu", "Brasserie Nationale",
    ],
    "other": [
        "Amazon", "Zalando", "IKEA", "H&M", "Decathlon",
        "Pharmacie", "Kinepolis", "Spotify", "Netflix", "Apple Store",
        "Bol.com", "Action",
    ],
}

FIRST_NAMES = [
    "Alex", "Camille", "Noor", "Robin", "Sam", "Lou",
    "Jules", "Charlie", "Morgan", "Ari", "Sacha", "Max",
]

LAST_NAMES = [
    "Peeters", "Janssens", "Maes", "Jacobs", "Mertens", "Willems",
    "Claes", "Goossens", "Wouters", "De Smet", "Dubois", "Lambert",
]


def _generate_percentages(randomizer: random.Random) -> dict[str, int]:
    """Generate 4 category percentages that sum to 100."""
    raw = [randomizer.randint(5, 60) for _ in range(4)]
    total = sum(raw)
    percentages = [max(1, round(r * 100 / total)) for r in raw]
    diff = 100 - sum(percentages)
    percentages[0] += diff
    return dict(zip(CATEGORIES, percentages))


def _generate_transactions(
    randomizer: random.Random,
    client_id: str,
    percentages: dict[str, int],
    count: int,
) -> list[dict[str, Any]]:
    """Generate a list of transactions for a customer."""
    categories = list(percentages.keys())
    weights = list(percentages.values())

    transactions: list[dict[str, Any]] = []
    for _ in range(count):
        category = randomizer.choices(categories, weights=weights, k=1)[0]
        merchant = randomizer.choice(MERCHANT_NAMES[category])

        if category == "mobility":
            amount = round(randomizer.uniform(1.50, 45.00), 2)
        elif category == "groceries":
            amount = round(randomizer.uniform(5.00, 120.00), 2)
        elif category == "bars_restaurants":
            amount = round(randomizer.uniform(8.00, 85.00), 2)
        else:
            amount = round(randomizer.uniform(3.00, 200.00), 2)

        transactions.append(
            {
                "client_id": client_id,
                "name": merchant,
                "amount": amount,
                "category": category,
            }
        )
    return transactions


def generate_clients(count: int, seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return deterministic customer profiles and their transactions."""
    if count < 0:
        raise ValueError("count must be zero or greater")

    randomizer = random.Random(seed)
    clients: list[dict[str, Any]] = []
    all_transactions: list[dict[str, Any]] = []

    for index in range(count):
        client_id = f"KBC-DEMO-{index + 1:06d}"
        first_name = randomizer.choice(FIRST_NAMES)
        last_name = randomizer.choice(LAST_NAMES)

        income = randomizer.randrange(1400, 6501, 100)
        spending = randomizer.randrange(900, min(5001, income + 1), 100)
        investment_balance = randomizer.randrange(0, 30001, 250)
        total_balance = randomizer.randrange(500, 50001, 250)

        percentages = _generate_percentages(randomizer)

        client: dict[str, Any] = {
            "client_id": client_id,
            "display_name": f"{first_name} {last_name}",
            "total_balance": total_balance,
            "income": income,
            "spending": spending,
            "investment_balance": investment_balance,
            "mobility_pct": percentages["mobility"],
            "groceries_pct": percentages["groceries"],
            "bars_restaurants_pct": percentages["bars_restaurants"],
            "other_pct": percentages["other"],
        }
        clients.append(client)

        tx_count = randomizer.randint(15, 40)
        all_transactions.extend(
            _generate_transactions(randomizer, client_id, percentages, tx_count)
        )

    return clients, all_transactions


def save_to_sqlite(
    clients: list[dict[str, Any]],
    transactions: list[dict[str, Any]],
    db_path: Path,
) -> None:
    """Replace all data in the SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        with connection:
            connection.executescript("""
                DROP TABLE IF EXISTS transactions;
                DROP TABLE IF EXISTS customers;

                CREATE TABLE customers (
                    client_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    total_balance REAL NOT NULL,
                    income REAL NOT NULL,
                    spending REAL NOT NULL,
                    investment_balance REAL NOT NULL,
                    mobility_pct INTEGER NOT NULL,
                    groceries_pct INTEGER NOT NULL,
                    bars_restaurants_pct INTEGER NOT NULL,
                    other_pct INTEGER NOT NULL
                );

                CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL CHECK (category IN ('mobility', 'groceries', 'bars_restaurants', 'other')),
                    FOREIGN KEY (client_id) REFERENCES customers (client_id)
                );

                CREATE INDEX idx_transactions_client ON transactions(client_id);
            """)

            connection.executemany(
                """
                INSERT INTO customers (
                    client_id, display_name, total_balance, income, spending,
                    investment_balance, mobility_pct, groceries_pct,
                    bars_restaurants_pct, other_pct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        c["client_id"],
                        c["display_name"],
                        c["total_balance"],
                        c["income"],
                        c["spending"],
                        c["investment_balance"],
                        c["mobility_pct"],
                        c["groceries_pct"],
                        c["bars_restaurants_pct"],
                        c["other_pct"],
                    )
                    for c in clients
                ],
            )

            connection.executemany(
                """
                INSERT INTO transactions (client_id, name, amount, category)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (t["client_id"], t["name"], t["amount"], t["category"])
                    for t in transactions
                ],
            )
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic KBC hackathon customer data with transactions."
    )
    parser.add_argument("--count", type=int, default=3, help="number of synthetic customers")
    parser.add_argument("--seed", type=int, default=42, help="random seed for reproducible demo data")
    parser.add_argument("--output", type=Path, default=Path("clients.json"), help="JSON output path")
    parser.add_argument("--db", type=Path, default=Path("clients.db"), help="SQLite database output path")
    args = parser.parse_args()

    clients, transactions = generate_clients(args.count, args.seed)

    output_data = {
        "clients": clients,
        "transactions": transactions,
    }
    args.output.write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    save_to_sqlite(clients, transactions, args.db)
    print(f"Wrote {len(clients)} clients and {len(transactions)} transactions to {args.output}")
    print(f"Seeded {len(clients)} clients and {len(transactions)} transactions into {args.db}")


if __name__ == "__main__":
    main()
