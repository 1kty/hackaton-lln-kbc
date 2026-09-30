"""Generate synthetic customer profiles for the KBC personalization hackathon."""

from __future__ import annotations

import argparse
import json
import random
import sqlite3
from pathlib import Path
from typing import Any


PERSONAS: list[dict[str, Any]] = [
    {
        "situation": "first_job",
        "age_band": "18-24",
        "life_stage": "first_job",
        "occupation": "employee",
        "products": ["current_account", "debit_card"],
        "signals": ["salary_payment_started", "mobile_app_active", "savings_balance_low"],
        "needs": ["build_emergency_savings", "understand_first_salary"],
        "next_best_action": "Offer a flexible monthly savings plan with a clear pause option.",
        "impact_goal": "Start a sustainable savings habit",
        "preferred_channel": "mobile_app",
        "contact_consent": True,
    },
    {
        "situation": "home_purchase",
        "age_band": "25-34",
        "life_stage": "planning_home_purchase",
        "occupation": "employee",
        "products": ["current_account", "savings_account", "debit_card"],
        "signals": ["mortgage_calculator_used", "property_search_payments", "savings_growing"],
        "needs": ["estimate_borrowing_capacity", "plan_purchase_costs"],
        "next_best_action": "Offer a mortgage readiness check and a transparent cost breakdown.",
        "impact_goal": "Make a confident, affordable home purchase",
        "preferred_channel": "mobile_app",
        "contact_consent": True,
    },
    {
        "situation": "cash_flow_pressure",
        "age_band": "35-44",
        "life_stage": "managing_monthly_budget",
        "occupation": "employee",
        "products": ["current_account", "credit_card", "home_insurance"],
        "signals": ["recurring_balance_dips", "bill_payment_late", "subscription_spending_increased"],
        "needs": ["avoid_overdraft", "regain_budget_visibility"],
        "next_best_action": "Privately offer a budget review and explain available support options.",
        "impact_goal": "Reduce financial stress without judgment",
        "preferred_channel": "secure_message",
        "contact_consent": True,
    },
    {
        "situation": "new_parent",
        "age_band": "25-34",
        "life_stage": "new_parent",
        "occupation": "employee",
        "products": ["current_account", "savings_account", "home_insurance"],
        "signals": ["family_related_recurring_spend", "new_savings_goal_created", "insurance_page_viewed"],
        "needs": ["plan_for_child_costs", "review_family_protection"],
        "next_best_action": "Offer an optional family financial check-in covering savings and protection.",
        "impact_goal": "Help plan for a new family expense horizon",
        "preferred_channel": "mobile_app",
        "contact_consent": True,
    },
    {
        "situation": "scam_concern",
        "age_band": "65+",
        "life_stage": "retired",
        "occupation": "retired",
        "products": ["current_account", "debit_card", "savings_account"],
        "signals": ["suspicious_transfer_reported", "security_help_page_viewed", "branch_visit_recent"],
        "needs": ["secure_account", "speak_to_trusted_support"],
        "next_best_action": "Show immediate security guidance and offer direct access to a human adviser.",
        "impact_goal": "Resolve a possible fraud concern quickly",
        "preferred_channel": "phone",
        "contact_consent": True,
    },
    {
        "situation": "student_budgeting",
        "age_band": "18-24",
        "life_stage": "student",
        "occupation": "student",
        "products": ["current_account", "debit_card"],
        "signals": ["education_payment_received", "small_frequent_card_payments", "budget_tool_opened"],
        "needs": ["manage_variable_income", "avoid_unexpected_fees"],
        "next_best_action": "Offer a lightweight spending overview and reminders the customer controls.",
        "impact_goal": "Build financial confidence while studying",
        "preferred_channel": "mobile_app",
        "contact_consent": True,
    },
    {
        "situation": "self_employed_income_variability",
        "age_band": "35-44",
        "life_stage": "self_employed",
        "occupation": "self_employed",
        "products": ["current_account", "business_account", "savings_account"],
        "signals": ["irregular_income", "tax_payment_due_soon", "invoice_paid_late"],
        "needs": ["smooth_income_volatility", "plan_tax_reserve"],
        "next_best_action": "Offer an opt-in cash-flow forecast with tax-date reminders.",
        "impact_goal": "Make variable income easier to plan",
        "preferred_channel": "web_banking",
        "contact_consent": True,
    },
    {
        "situation": "sustainable_renovation",
        "age_band": "35-44",
        "life_stage": "homeowner_planning_renovation",
        "occupation": "employee",
        "products": ["current_account", "home_loan", "home_insurance"],
        "signals": ["energy_bill_increased", "renovation_information_viewed", "green_finance_page_viewed"],
        "needs": ["compare_renovation_financing", "understand_energy_savings"],
        "next_best_action": "Present relevant renovation financing information and independent planning tools.",
        "impact_goal": "Support an informed energy-efficiency project",
        "preferred_channel": "web_banking",
        "contact_consent": True,
    },
    {
        "situation": "moving_abroad",
        "age_band": "25-34",
        "life_stage": "planning_international_move",
        "occupation": "employee",
        "products": ["current_account", "debit_card", "travel_insurance"],
        "signals": ["international_transfers_increased", "travel_card_controls_viewed", "address_update_started"],
        "needs": ["manage_cross_border_banking", "understand_card_and_transfer_fees"],
        "next_best_action": "Offer a move checklist with country-specific account and payment information.",
        "impact_goal": "Avoid disruption during an international move",
        "preferred_channel": "mobile_app",
        "contact_consent": True,
    },
    {
        "situation": "first_time_investing",
        "age_band": "25-34",
        "life_stage": "building_long_term_savings",
        "occupation": "employee",
        "products": ["current_account", "savings_account"],
        "signals": ["investment_basics_viewed", "regular_savings_established", "risk_profile_not_completed"],
        "needs": ["understand_investment_risk", "compare_long_term_options"],
        "next_best_action": "Offer neutral investment education and a risk-profile flow before any product proposal.",
        "impact_goal": "Support informed decisions without pressure",
        "preferred_channel": "mobile_app",
        "contact_consent": False,
    },
    {
        "situation": "insurance_claim_support",
        "age_band": "45-54",
        "life_stage": "handling_home_damage",
        "occupation": "employee",
        "products": ["current_account", "home_loan", "home_insurance"],
        "signals": ["claim_started", "claim_status_checked_repeatedly", "support_contact_requested"],
        "needs": ["understand_claim_status", "know_next_required_step"],
        "next_best_action": "Provide a clear claim status, next step, and one-tap route to the claims team.",
        "impact_goal": "Reduce uncertainty while resolving a claim",
        "preferred_channel": "secure_message",
        "contact_consent": True,
    },
    {
        "situation": "prefers_human_support",
        "age_band": "55-64",
        "life_stage": "planning_retirement",
        "occupation": "employee",
        "products": ["current_account", "savings_account", "pension_savings"],
        "signals": ["retirement_planning_page_viewed", "digital_flow_abandoned", "branch_appointment_requested"],
        "needs": ["understand_retirement_income", "get_personal_explanation"],
        "next_best_action": "Offer an adviser appointment and preserve progress from the digital journey.",
        "impact_goal": "Make complex planning accessible across channels",
        "preferred_channel": "branch",
        "contact_consent": True,
    },
]

FIRST_NAMES = ["Alex", "Camille", "Noor", "Robin", "Sam", "Lou", "Jules", "Charlie", "Morgan", "Ari", "Sacha", "Max"]


def generate_clients(count: int, seed: int) -> list[dict[str, Any]]:
    """Return deterministic, fictional customer profiles for demos and tests."""
    if count < 0:
        raise ValueError("count must be zero or greater")

    randomizer = random.Random(seed)
    clients = []
    for index in range(count):
        persona = PERSONAS[index % len(PERSONAS)]
        client = dict(persona)
        client["products"] = list(persona["products"])
        client["signals"] = list(persona["signals"])
        client["needs"] = list(persona["needs"])
        client["client_id"] = f"KBC-DEMO-{index + 1:06d}"
        client["display_name"] = f"{randomizer.choice(FIRST_NAMES)} {index + 1:04d}"
        client["monthly_income_eur"] = randomizer.randrange(1400, 6501, 100)
        client["monthly_expenses_eur"] = randomizer.randrange(900, 5001, 100)
        client["savings_balance_eur"] = randomizer.randrange(0, 50001, 250)
        clients.append(client)
    return clients


def save_clients_to_sqlite(clients: list[dict[str, Any]], db_path: Path) -> None:
    """Replace the synthetic demo records in a SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    client_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    situation TEXT NOT NULL,
                    age_band TEXT NOT NULL,
                    life_stage TEXT NOT NULL,
                    occupation TEXT NOT NULL,
                    products TEXT NOT NULL,
                    signals TEXT NOT NULL,
                    needs TEXT NOT NULL,
                    next_best_action TEXT NOT NULL,
                    impact_goal TEXT NOT NULL,
                    preferred_channel TEXT NOT NULL,
                    contact_consent INTEGER NOT NULL CHECK (contact_consent IN (0, 1)),
                    monthly_income_eur INTEGER NOT NULL,
                    monthly_expenses_eur INTEGER NOT NULL,
                    savings_balance_eur INTEGER NOT NULL
                )
                """
            )
            connection.execute("DELETE FROM customers")
            connection.executemany(
                """
                INSERT INTO customers VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                [
                    (
                        client["client_id"],
                        client["display_name"],
                        client["situation"],
                        client["age_band"],
                        client["life_stage"],
                        client["occupation"],
                        json.dumps(client["products"], ensure_ascii=False),
                        json.dumps(client["signals"], ensure_ascii=False),
                        json.dumps(client["needs"], ensure_ascii=False),
                        client["next_best_action"],
                        client["impact_goal"],
                        client["preferred_channel"],
                        int(client["contact_consent"]),
                        client["monthly_income_eur"],
                        client["monthly_expenses_eur"],
                        client["savings_balance_eur"],
                    )
                    for client in clients
                ],
            )
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic KBC hackathon customer data.")
    parser.add_argument("--count", type=int, default=len(PERSONAS), help="number of synthetic customers (default: one per persona)")
    parser.add_argument("--seed", type=int, default=42, help="random seed for reproducible demo data")
    parser.add_argument("--output", type=Path, default=Path("clients.json"), help="JSON output path")
    parser.add_argument("--db", type=Path, default=Path("clients.db"), help="SQLite database output path")
    args = parser.parse_args()

    clients = generate_clients(args.count, args.seed)
    args.output.write_text(json.dumps(clients, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_clients_to_sqlite(clients, args.db)
    print(f"Wrote {len(clients)} synthetic clients to {args.output}")
    print(f"Seeded {len(clients)} synthetic clients into {args.db}")


if __name__ == "__main__":
    main()
