import {
  ArrowDownLeftIcon,
  ArrowUpRightIcon,
  CarIcon,
  PiggyBankIcon,
  ShoppingBasketIcon,
  UtensilsIcon,
  WalletIcon,
} from "lucide-react"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { formatEuro } from "@/lib/format"
import { cn } from "cn"
import type { Customer } from "@/lib/api"

export function MonthlyOverview({
  customer,
  className,
}: {
  customer: Customer
  className?: string
}) {
  const summary = [
    {
      label: "Revenus",
      amount: customer.income,
      icon: ArrowDownLeftIcon,
    },
    {
      label: "Dépenses",
      amount: customer.spending,
      icon: ArrowUpRightIcon,
    },
    {
      label: "Investir",
      amount: customer.investment_balance,
      icon: PiggyBankIcon,
    },
  ] as const

  const categories = [
    {
      label: "Mobilité",
      percent: customer.mobility_pct,
      amount: (customer.spending * customer.mobility_pct) / 100,
      icon: CarIcon,
    },
    {
      label: "Courses",
      percent: customer.groceries_pct,
      amount: (customer.spending * customer.groceries_pct) / 100,
      icon: ShoppingBasketIcon,
    },
    {
      label: "Bars & restaurants",
      percent: customer.bars_restaurants_pct,
      amount: (customer.spending * customer.bars_restaurants_pct) / 100,
      icon: UtensilsIcon,
    },
    {
      label: "Autres dépenses",
      percent: customer.other_pct,
      amount: (customer.spending * customer.other_pct) / 100,
      icon: WalletIcon,
    },
  ] as const

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardDescription>Aperçu mensuel</CardDescription>
        <CardTitle className="text-xl font-semibold tracking-tight">
          Septembre 2026
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid gap-3 sm:grid-cols-3">
          {summary.map((item) => (
            <div
              key={item.label}
              className="flex items-start gap-3 rounded-xl bg-muted/50 p-3 ring-1 ring-foreground/5"
            >
              <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <item.icon className="size-4" />
              </div>
              <div className="min-w-0">
                <p className="text-xs text-muted-foreground">{item.label}</p>
                <p className="truncate text-base font-semibold tabular-nums">
                  {formatEuro(item.amount)}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-4">
          <p className="text-sm font-medium">Répartition des dépenses</p>
          {categories.map((category) => (
            <div key={category.label} className="space-y-2">
              <div className="flex items-center justify-between gap-3 text-sm">
                <div className="flex min-w-0 items-center gap-2">
                  <category.icon className="size-4 shrink-0 text-muted-foreground" />
                  <span className="truncate">{category.label}</span>
                </div>
                <div className="flex shrink-0 items-center gap-3 tabular-nums">
                  <span className="text-muted-foreground">
                    {formatEuro(category.amount)}
                  </span>
                  <span className="w-10 text-right font-medium">
                    {category.percent}&nbsp;%
                  </span>
                </div>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-primary transition-all"
                  style={{ width: `${category.percent}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
