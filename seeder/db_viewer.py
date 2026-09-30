"""Streamlit viewer for the synthetic customer SQLite database."""

import json
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
    situations = [row[0] for row in connection.execute("SELECT DISTINCT situation FROM customers ORDER BY situation")]
    channels = [row[0] for row in connection.execute("SELECT DISTINCT preferred_channel FROM customers ORDER BY preferred_channel")]

    st.sidebar.header("Filtres")
    search = st.sidebar.text_input("Recherche", placeholder="ID ou nom")
    selected_situation = st.sidebar.selectbox("Situation", ["Toutes", *situations])
    selected_channel = st.sidebar.selectbox("Canal préféré", ["Tous", *channels])
    page_size = st.sidebar.selectbox("Profils par page", [10, 25, 50, 100], index=1)

    conditions = []
    parameters: list[str] = []
    if search:
        conditions.append("(client_id LIKE ? OR display_name LIKE ?)")
        parameters.extend([f"%{search}%", f"%{search}%"])
    if selected_situation != "Toutes":
        conditions.append("situation = ?")
        parameters.append(selected_situation)
    if selected_channel != "Tous":
        conditions.append("preferred_channel = ?")
        parameters.append(selected_channel)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    matching_count = connection.execute(
        f"SELECT COUNT(*) FROM customers {where_clause}", parameters
    ).fetchone()[0]
    opted_in_count = connection.execute(
        f"SELECT COUNT(*) FROM customers {where_clause} {'AND' if where_clause else 'WHERE'} contact_consent = 1",
        parameters,
    ).fetchone()[0]

    metrics = st.columns(2)
    metrics[0].metric("Profils correspondants", matching_count)
    metrics[1].metric("Avec consentement de contact", opted_in_count)

    page_count = max(1, (matching_count + page_size - 1) // page_size)
    page_number = st.sidebar.number_input("Page", min_value=1, max_value=page_count, value=1)
    records = connection.execute(
        f"""
        SELECT client_id, display_name, situation, age_band, occupation,
               preferred_channel, contact_consent, monthly_income_eur,
               monthly_expenses_eur, savings_balance_eur
        FROM customers {where_clause}
        ORDER BY client_id
        LIMIT ? OFFSET ?
        """,
        [*parameters, page_size, (page_number - 1) * page_size],
    ).fetchall()

    if records:
        table_rows = [
            {
                "ID": row["client_id"],
                "Client": row["display_name"],
                "Situation": row["situation"],
                "Tranche d'âge": row["age_band"],
                "Profession": row["occupation"],
                "Canal préféré": row["preferred_channel"],
                "Consentement": "Oui" if row["contact_consent"] else "Non",
                "Revenus mensuels (€)": row["monthly_income_eur"],
                "Dépenses mensuelles (€)": row["monthly_expenses_eur"],
                "Épargne (€)": row["savings_balance_eur"],
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
        for field in ("products", "signals", "needs"):
            profile[field] = json.loads(profile[field])
        profile["contact_consent"] = bool(profile["contact_consent"])
        with st.expander("Signaux, besoins et accompagnement proposé", expanded=True):
            st.json(profile)
    else:
        st.info("Aucun profil ne correspond à ces filtres.")
finally:
    connection.close()
