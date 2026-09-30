import {
  CarIcon,
  CoffeeIcon,
  ShoppingBasketIcon,
  SmartphoneIcon,
  UtensilsIcon,
  type LucideIcon,
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
import type { Transaction } from "@/lib/api"

const CATEGORY_ICONS: Record<string, LucideIcon> = {
  mobility: CarIcon,
  groceries: ShoppingBasketIcon,
  bars_restaurants: CoffeeIcon,
  other: SmartphoneIcon,
}

const CATEGORY_LABELS: Record<string, string> = {
  mobility: "Mobilité",
  groceries: "Courses",
  bars_restaurants: "Bars & restaurants",
  other: "Autres",
}

export function ExpenseList({
  transactions,
  className,
}: {
  transactions: Transaction[]
  className?: string
}) {
  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardDescription>Dernières opérations</CardDescription>
        <CardTitle className="text-xl font-semibold tracking-tight">
          Liste des dépenses
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="divide-y divide-border">
          {transactions.map((tx) => {
            const Icon = CATEGORY_ICONS[tx.category] ?? SmartphoneIcon
            return (
              <li
                key={tx.id}
                className="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
              >
                <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-foreground text-background">
                  <Icon className="size-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium">{tx.name}</p>
                  <p className="truncate text-xs text-muted-foreground">
                    {CATEGORY_LABELS[tx.category] ?? tx.category}
                  </p>
                </div>
                <p className="shrink-0 text-sm font-semibold tabular-nums text-foreground">
                  −{formatEuro(tx.amount)}
                </p>
              </li>
            )
          })}
        </ul>
      </CardContent>
    </Card>
  )
}
