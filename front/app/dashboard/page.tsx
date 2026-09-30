"use client"

import * as React from "react"
import { BalanceCard } from "@/components/balance-card"
import { ExpenseList } from "@/components/expense-list"
import { FinanceAssistant } from "@/components/finance-assistant"
import { KbcLogo } from "@/components/kbc-logo"
import { MonthlyOverview } from "@/components/monthly-overview"
import { ThemeToggle } from "@/components/theme-toggle"
import { fetchCustomer, type Customer } from "@/lib/api"

const CLIENT_ID = "KBC-DEMO-000001"

export default function Page() {
  const [customer, setCustomer] = React.useState<Customer | null>(null)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    fetchCustomer(CLIENT_ID)
      .then(setCustomer)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return <div className="m-5 text-destructive">Error: {error}</div>
  }

  if (!customer) {
    return <div className="m-5 text-muted-foreground">Loading…</div>
  }

  return (
    <div className="m-5 space-y-5 pb-24">
      <header className="flex items-center justify-between gap-4">
        <KbcLogo />
        <div className="flex items-center gap-3">
          <p className="hidden text-sm text-muted-foreground sm:block">
            Vue d&apos;ensemble
          </p>
          <ThemeToggle />
        </div>
      </header>

      <div className="grid gap-5 lg:grid-cols-2">
        <BalanceCard
          balance={customer.total_balance}
          cardHolder={customer.display_name}
        />
        <MonthlyOverview customer={customer} />
      </div>
      <ExpenseList transactions={customer.transactions} />

      <FinanceAssistant clientId={CLIENT_ID} />
    </div>
  )
}
