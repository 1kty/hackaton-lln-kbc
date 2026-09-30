"use client"

import * as React from "react"
import { MoonIcon, SunIcon } from "lucide-react"
import { useTheme } from "next-themes"
import { cn } from "cn"

import { Button } from "@/components/ui/button"

export function ThemeToggle({ className }: { className?: string }) {
  const { resolvedTheme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  const isDark = mounted && resolvedTheme === "dark"

  return (
    <Button
      type="button"
      variant="outline"
      size="icon"
      className={cn("rounded-full", className)}
      aria-label={
        !mounted
          ? "Changer le thème"
          : isDark
            ? "Passer en mode clair"
            : "Passer en mode sombre"
      }
      onClick={() => {
        if (!mounted) return
        setTheme(isDark ? "light" : "dark")
      }}
    >
      <SunIcon className={cn("size-4", isDark ? "hidden" : "block")} />
      <MoonIcon className={cn("size-4", isDark ? "block" : "hidden")} />
    </Button>
  )
}
