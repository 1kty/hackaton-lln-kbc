"""Streamlit viewer for the synthetic customer SQLite database."""

import sqlite3
from pathlib import Path

import streamlit as st


DATABASE_PATH = Path(__file__).with_name("clients.db")

st.set_page_config(page_title="KBC | Clients", page_icon="K", layout="wide")
st.title("Explorateur des clients")
st.caption("Profils synthétiques pour le prototype du hackathon KBC")

if not DATABASE_PATH.exists():
    st.warning("Base introuvable. Générez-la avec : python seed_clients.py --count 100")
    st.stop()

connection = sqlite3.connect(DATABASE_PATH)
connection.row_factory = sqlite3.Row

try:
    categories = [row[0] for row in connection.execute("SELECT DISTINCT category FROM transactions ORDER BY category")]

    st.sidebar.header("Filtres")
    search = st.sidebar.text_input("Recherche", placeholder="ID ou nom")
    selected_category = st.sidebar.selectbox("Catégorie", ["Toutes", *categories])
    page_size = st.sidebar.selectbox("Profils par page", [10, 25, 50, 100], index=1)

    conditions = []
    parameters: list[str] = []
    if search:
        conditions.append("(c.client_id LIKE ? OR c.display_name LIKE ?)")
        parameters.extend([f"%{search}%", f"%{search}%"])
    if selected_category != "Toutes":
        conditions.append(
            "c.client_id IN (SELECT DISTINCT client_id FROM transactions WHERE category = ?)"
        )
        parameters.append(selected_category)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    matching_count = connection.execute(
        f"SELECT COUNT(*) FROM customers c {where_clause}", parameters
    ).fetchone()[0]
    tx_count = connection.execute(
        f"SELECT COUNT(*) FROM transactions t JOIN customers c ON t.client_id = c.client_id {where_clause}",
        parameters,
    ).fetchone()[0]

    metrics = st.columns(3)
    metrics[0].metric("Profils correspondants", matching_count)
    metrics[1].metric("Transactions", tx_count)
    metrics[2].metric("Categories", len(categories))

    page_count = max(1, (matching_count + page_size - 1) // page_size)
    page_number = st.sidebar.number_input("Page", min_value=1, max_value=page_count, value=1)
    records = connection.execute(
        f"""
        SELECT c.client_id, c.display_name, c.total_balance, c.income, c.spending,
               c.investment_balance, c.mobility_pct, c.groceries_pct,
               c.bars_restaurants_pct, c.other_pct
        FROM customers c {where_clause}
        ORDER BY c.client_id
        LIMIT ? OFFSET ?
        """,
        [*parameters, page_size, (page_number - 1) * page_size],
    ).fetchall()

    if records:
        table_rows = [
            {
                "ID": row["client_id"],
                "Client": row["display_name"],
                "Balance (€)": f"{row['total_balance']:,.2f}",
                "Income (€)": f"{row['income']:,.2f}",
                "Spending (€)": f"{row['spending']:,.2f}",
                "Investment (€)": f"{row['investment_balance']:,.2f}",
                "Mobility %": row["mobility_pct"],
                "Groceries %": row["groceries_pct"],
                "Bars & Rest. %": row["bars_restaurants_pct"],
                "Other %": row["other_pct"],
            }
            for row in records
        ]
        st.dataframe(table_rows, use_container_width=True, hide_index=True)

        selected_id = st.selectbox(
            "Détail du profil",
            [row["client_id"] for row in records],
            format_func=lambda client_id: next(
                f"{row['display_name']} · {client_id}" for row in records if row["client_id"] == client_id
            ),
        )
        detail = connection.execute(
            "SELECT * FROM customers WHERE client_id = ?", (selected_id,)
        ).fetchone()
        profile = dict(detail)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.json(profile)
        with col2:
            transactions = connection.execute(
                "SELECT name, amount, category FROM transactions WHERE client_id = ? ORDER BY id",
                (selected_id,),
            ).fetchall()
            tx_rows = [
                {"Name": t["name"], "Amount (€)": f"{t['amount']:.2f}", "Category": t["category"]}
                for t in transactions
            ]
            st.dataframe(tx_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun profil ne correspond à ces filtres.")
finally:
    connection.close()
