/** Stable EUR formatting for SSR + client (avoids Intl space mismatches). */
export function formatEuro(amount: number, currency = "EUR") {
  const absolute = Math.abs(amount)
  const fixed = absolute.toFixed(2)
  const [intPart, decPart] = fixed.split(".")
  const withSpaces = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, " ")
  const sign = amount < 0 ? "−" : ""
  return `${sign}${withSpaces},${decPart}\u00a0${currency === "EUR" ? "€" : currency}`
}
