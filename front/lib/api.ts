const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export type Transaction = {
  id: number
  name: string
  amount: number
  category: string
}

export type Customer = {
  client_id: string
  display_name: string
  total_balance: number
  income: number
  spending: number
  investment_balance: number
  mobility_pct: number
  groceries_pct: number
  bars_restaurants_pct: number
  other_pct: number
  transactions: Transaction[]
}

export type ChatMessage = {
  role: "user" | "assistant"
  content: string
}

export async function fetchCustomer(clientId: string): Promise<Customer> {
  const res = await fetch(`${API_URL}/api/customers/${clientId}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function sendChatMessage(
  clientId: string,
  message: string,
  history: ChatMessage[]
): Promise<string> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ client_id: clientId, message, history }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  const data = await res.json()
  return data.reply
}
