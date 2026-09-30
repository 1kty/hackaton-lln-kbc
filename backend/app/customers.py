from typing import Any

from backend.app.db import connect


def get_customer(client_id: str) -> dict[str, Any] | None:
    connection = connect()
    try:
        row = connection.execute(
            "SELECT * FROM customers WHERE client_id = ?",
            (client_id,),
        ).fetchone()
    finally:
        connection.close()

    if row is None:
        return None

    return dict(row)


def get_transactions(client_id: str) -> list[dict[str, Any]]:
    connection = connect()
    try:
        rows = connection.execute(
            "SELECT id, name, amount, category FROM transactions WHERE client_id = ? ORDER BY id",
            (client_id,),
        ).fetchall()
    finally:
        connection.close()

    return [dict(row) for row in rows]
