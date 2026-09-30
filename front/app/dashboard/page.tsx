import { BalanceCard } from "@/components/balance-card"
import { ExpenseList } from "@/components/expense-list"
import { FinanceAssistant } from "@/components/finance-assistant"
import { KbcLogo } from "@/components/kbc-logo"
import { MonthlyOverview } from "@/components/monthly-overview"
import { ThemeToggle } from "@/components/theme-toggle"

export default function Page() {
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
          balance={3847.62}
          currency="EUR"
          cardHolder="Sophie Laurent"
          cardNumber="4532 8814 2091 7743"
          expiry="11/28"
        />
        <MonthlyOverview />
      </div>
      <ExpenseList />

      <FinanceAssistant />
    </div>
  )
}
