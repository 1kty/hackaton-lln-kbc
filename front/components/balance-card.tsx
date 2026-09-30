import { cn } from "cn"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { formatEuro } from "@/lib/format"

type BalanceCardProps = {
  balance?: number
  currency?: string
  cardHolder?: string
  cardNumber?: string
  expiry?: string
  className?: string
}

function maskCardNumber(cardNumber: string) {
  const digits = cardNumber.replace(/\s/g, "")
  const lastFour = digits.slice(-4)
  return `•••• •••• •••• ${lastFour}`
}

export function BalanceCard({
  balance = 2480.5,
  currency = "EUR",
  cardHolder = "Jean Dupont",
  cardNumber = "4532 1189 7741 9021",
  expiry = "09/28",
  className,
}: BalanceCardProps) {
  return (
    <Card className={cn("w-full p-3", className)}>
      <CardHeader>
        <div className="flex items-center justify-between gap-2">
          <CardDescription>Balance</CardDescription>
          <span className="flex items-center gap-x-2 rounded-2xl bg-muted px-4 py-2 text-lg font-medium text-muted-foreground">
            {currency}
            <div className="h-6 w-6 overflow-hidden">
              <img
                className="h-full w-full rounded-lg object-cover"
                src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg"
                alt=""
              />
            </div>
          </span>
        </div>
        <CardTitle className="text-3xl font-semibold tracking-tight tabular-nums">
          {formatEuro(balance, currency)}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative aspect-16/10 max-w-md overflow-hidden rounded-2xl bg-linear-to-br from-kbc-navy-600 via-kbc-navy to-kbc-blue p-5 text-white shadow-lg transition-shadow hover:shadow-xl hover:shadow-kbc-blue/30">
          <div className="pointer-events-none absolute -top-10 -right-10 size-40 rounded-full bg-white/10 blur-2xl" />
          <div className="pointer-events-none absolute -bottom-12 -left-8 size-36 rounded-full bg-kbc-blue/40 blur-2xl" />

          <div className="relative flex h-full flex-col justify-between">
            <div className="flex items-start justify-between">
              <span className="text-xs font-medium tracking-[0.2em] uppercase opacity-80">
                Virtual
              </span>
              <div className="flex h-8 w-11 items-center justify-center rounded-md bg-linear-to-br from-amber-200 to-amber-400 shadow-sm">
                <div className="h-5 w-8 rounded-[2px] border border-amber-600/30 bg-linear-to-br from-amber-300/80 to-amber-500/80" />
              </div>
            </div>

            <p className="font-mono text-lg tracking-widest tabular-nums">
              {maskCardNumber(cardNumber)}
            </p>

            <div className="flex items-end justify-between gap-4">
              <div className="min-w-0">
                <p className="text-[10px] tracking-wider uppercase opacity-60">
                  Card holder
                </p>
                <p className="truncate text-sm font-medium tracking-wide uppercase">
                  {cardHolder}
                </p>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-[10px] tracking-wider uppercase opacity-60">
                  Exp
                </p>
                <p className="font-mono text-sm tabular-nums">{expiry}</p>
              </div>
            </div>
          </div>
        </div>
        
      </CardContent>
    </Card>
  )
}
