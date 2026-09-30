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

type Expense = {
  id: string
  label: string
  category: string
  date: string
  amount: number
  icon: LucideIcon
}

const expenses: Expense[] = [
  {
    id: "1",
    label: "Carrefour Market",
    category: "Courses",
    date: "29 sept.",
    amount: 64.32,
    icon: ShoppingBasketIcon,
  },
  {
    id: "2",
    label: "STIB — abonnement",
    category: "Mobilité",
    date: "28 sept.",
    amount: 49.0,
    icon: CarIcon,
  },
  {
    id: "3",
    label: "Café Belga",
    category: "Bars & restaurants",
    date: "27 sept.",
    amount: 18.5,
    icon: CoffeeIcon,
  },
  {
    id: "4",
    label: "Le Pain Quotidien",
    category: "Bars & restaurants",
    date: "26 sept.",
    amount: 27.8,
    icon: UtensilsIcon,
  },
  {
    id: "5",
    label: "Proximus",
    category: "Autres",
    date: "25 sept.",
    amount: 35.99,
    icon: SmartphoneIcon,
  },
  {
    id: "6",
    label: "Delhaize",
    category: "Courses",
    date: "24 sept.",
    amount: 52.14,
    icon: ShoppingBasketIcon,
  },
]

export function ExpenseList({ className }: { className?: string }) {
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
          {expenses.map((expense) => (
            <li
              key={expense.id}
              className="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
            >
              <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-foreground text-background">
                <expense.icon className="size-4" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">{expense.label}</p>
                <p className="truncate text-xs text-muted-foreground">
                  {expense.category} · {expense.date}
                </p>
              </div>
              <p className="shrink-0 text-sm font-semibold tabular-nums text-foreground">
                −{formatEuro(expense.amount)}
              </p>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
