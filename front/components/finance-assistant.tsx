"use client"

import * as React from "react"
import { SendIcon, SparklesIcon, XIcon } from "lucide-react"
import { cn } from "cn"

import { Bubble, BubbleContent } from "@/components/ui/bubble"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {
  Message,
  MessageAvatar,
  MessageContent,
  MessageHeader,
} from "@/components/ui/message"
import {
  MessageScroller,
  MessageScrollerButton,
  MessageScrollerContent,
  MessageScrollerItem,
  MessageScrollerProvider,
  MessageScrollerViewport,
} from "@/components/ui/message-scroller"
import { sendChatMessage } from "@/lib/api"

type ChatMessage = {
  id: string
  role: "assistant" | "user"
  content: string
}

const SUGGESTIONS = [
  "Où puis-je économiser ce mois-ci ?",
  "Analyse mes dépenses restaurants",
  "Puis-je investir davantage ?",
  "Résume mon budget",
]

function AssistantMascot({ className }: { className?: string }) {
  return (
    <img className="rounded-full" src="banker.png"/>
  )
}

function formatMessage(content: string) {
  return content.split("\n").map((line, i) => {
    const parts = line.split(/(\*\*[^*]+\*\*)/g)
    return (
      <React.Fragment key={i}>
        {i > 0 ? <br /> : null}
        {parts.map((part, j) => {
          if (part.startsWith("**") && part.endsWith("**")) {
            return (
              <strong key={j} className="font-semibold">
                {part.slice(2, -2)}
              </strong>
            )
          }
          return <React.Fragment key={j}>{part}</React.Fragment>
        })}
      </React.Fragment>
    )
  })
}

export function FinanceAssistant({ clientId }: { clientId: string }) {
  const [open, setOpen] = React.useState(false)
  const [input, setInput] = React.useState("")
  const [typing, setTyping] = React.useState(false)
  const [messages, setMessages] = React.useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Salut ! Je suis Bryan, ton assistant KBC. J'analyse ton solde, tes dépenses et tes investissements pour te proposer une aide ciblée. Que veux-tu simplifier aujourd'hui ?",
    },
  ])

  async function sendMessage(text: string) {
    const trimmed = text.trim()
    if (!trimmed || typing) return

    const userMessage: ChatMessage = {
      id: `u-${Date.now()}`,
      role: "user",
      content: trimmed,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setTyping(true)

    try {
      const reply = await sendChatMessage(clientId, trimmed, messages)
      setMessages((prev) => [
        ...prev,
        {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: reply,
        },
      ])
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: "Désolé, une erreur est survenue. Réessaie dans un instant.",
        },
      ])
    } finally {
      setTyping(false)
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Ouvrir l'assistant Bryan"
        className={cn(
          "fixed right-5 bottom-5 z-40 flex size-16 items-center justify-center rounded-full",
          "bg-card shadow-lg ring-2 ring-primary/30",
          "transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:ring-primary",
          "active:scale-95",
          open && "pointer-events-none scale-90 opacity-0"
        )}
      >
        <AssistantMascot className="size-14" />
        <span className="absolute -top-0.5 -right-0.5 flex size-4">
          <span className="absolute inline-flex size-full animate-ping rounded-full bg-primary opacity-60" />
          <span className="relative inline-flex size-4 rounded-full bg-primary ring-2 ring-card" />
        </span>
      </button>

      {open ? (
        <Card
          className={cn(
            "fixed right-4 bottom-4 z-50 flex h-[min(36rem,calc(100vh-2rem))] w-[min(100%-2rem,24rem)] flex-col gap-0 py-0",
            "shadow-2xl"
          )}
        >
          <CardHeader className="flex flex-row items-center gap-3 space-y-0 rounded-t-xl bg-linear-to-r from-kbc-navy to-kbc-blue px-4 py-3 text-white">
            <div className="flex size-11 items-center justify-center rounded-full bg-white/15 ring-1 ring-white/25">
              <AssistantMascot className="size-10" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="font-semibold leading-tight text-white">Bryan</p>
              <p className="flex items-center gap-1 text-xs text-white/80">
                <SparklesIcon className="size-3" />
                Aide ciblée · données analysées
              </p>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="icon-sm"
              onClick={() => setOpen(false)}
              className="text-white hover:bg-white/15 hover:text-white"
              aria-label="Fermer le chat"
            >
              <XIcon />
            </Button>
          </CardHeader>

          <CardContent className="flex min-h-0 flex-1 flex-col p-0">
            <MessageScrollerProvider
              autoScroll
              defaultScrollPosition="last-anchor"
              scrollPreviousItemPeek={48}
            >
              <MessageScroller className="min-h-0 flex-1 bg-muted/40">
                <MessageScrollerViewport>
                  <MessageScrollerContent className="gap-4 p-4">
                    {messages.map((message) => {
                      const isUser = message.role === "user"
                      return (
                        <MessageScrollerItem
                          key={message.id}
                          messageId={message.id}
                          scrollAnchor={isUser}
                        >
                          <Message align={isUser ? "end" : "start"}>
                            {!isUser ? (
                              <MessageAvatar className="size-8 bg-card ring-1 ring-border">
                                <AssistantMascot className="size-7" />
                              </MessageAvatar>
                            ) : null}
                            <MessageContent>
                              {!isUser ? (
                                <MessageHeader>Bryan</MessageHeader>
                              ) : null}
                              <Bubble
                                variant={isUser ? "default" : "secondary"}
                                align={isUser ? "end" : "start"}
                              >
                                <BubbleContent>
                                  {formatMessage(message.content)}
                                </BubbleContent>
                              </Bubble>
                            </MessageContent>
                          </Message>
                        </MessageScrollerItem>
                      )
                    })}

                    {typing ? (
                      <MessageScrollerItem messageId="typing">
                        <Message align="start">
                          <MessageAvatar className="size-8 bg-card ring-1 ring-border">
                            <AssistantMascot className="size-7" />
                          </MessageAvatar>
                          <MessageContent>
                            <Bubble variant="secondary" align="start">
                              <BubbleContent className="flex items-center gap-1 py-3">
                                <span className="size-1.5 animate-bounce rounded-full bg-primary [animation-delay:0ms]" />
                                <span className="size-1.5 animate-bounce rounded-full bg-primary [animation-delay:150ms]" />
                                <span className="size-1.5 animate-bounce rounded-full bg-primary [animation-delay:300ms]" />
                              </BubbleContent>
                            </Bubble>
                          </MessageContent>
                        </Message>
                      </MessageScrollerItem>
                    ) : null}

                    {messages.length <= 1 && !typing ? (
                      <MessageScrollerItem messageId="suggestions">
                        <div className="flex flex-wrap gap-2 pl-10">
                          {SUGGESTIONS.map((suggestion) => (
                            <Button
                              key={suggestion}
                              type="button"
                              variant="outline"
                              size="xs"
                              className="h-auto rounded-full px-3 py-1.5 text-left whitespace-normal"
                              onClick={() => sendMessage(suggestion)}
                            >
                              {suggestion}
                            </Button>
                          ))}
                        </div>
                      </MessageScrollerItem>
                    ) : null}
                  </MessageScrollerContent>
                </MessageScrollerViewport>
                <MessageScrollerButton />
              </MessageScroller>
            </MessageScrollerProvider>
          </CardContent>

          <CardFooter className="border-t p-3">
            <form
              className="flex w-full items-center gap-2"
              onSubmit={(event) => {
                event.preventDefault()
                sendMessage(input)
              }}
            >
              <Input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Pose ta question…"
                className="h-10 flex-1 rounded-xl bg-muted/40"
                aria-label="Message à Bryan"
              />
              <Button
                type="submit"
                size="icon-lg"
                className="rounded-xl"
                disabled={!input.trim() || typing}
                aria-label="Envoyer"
              >
                <SendIcon />
              </Button>
            </form>
          </CardFooter>
        </Card>
      ) : null}
    </>
  )
}
