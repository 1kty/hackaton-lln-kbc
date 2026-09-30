import Image from "next/image"
import Link from "next/link"

import { cn } from "cn"

type KbcLogoProps = {
  className?: string
  showWordmark?: boolean
  asLink?: boolean
}

export function KbcLogo({
  className,
  showWordmark = true,
  asLink = true,
}: KbcLogoProps) {
  const content = (
    <>
      <Image
        src="/kbc-logo.svg"
        alt=""
        width={40}
        height={40}
        className="size-10"
        priority
      />
      {showWordmark ? (
        <span className="text-xl font-bold tracking-tight text-foreground">
          KBC
        </span>
      ) : null}
    </>
  )

  if (!asLink) {
    return (
      <span className={cn("inline-flex items-center gap-2.5", className)}>
        {content}
      </span>
    )
  }

  return (
    <Link
      href="/dashboard"
      className={cn("inline-flex items-center gap-2.5", className)}
      aria-label="KBC"
    >
      {content}
    </Link>
  )
}
