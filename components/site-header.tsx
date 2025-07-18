"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FileText, BookOpen, Calendar, FileCode, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { ModeToggle } from "./mode-toggle";

const navigation = [
  { name: "Dashboard", href: "/", exact: true },
  { name: "Editor", href: "/editor", icon: FileText },
  { name: "Contexts", href: "/contexts", icon: Calendar },
  { name: "Taxonomy", href: "/taxonomy", icon: BookOpen },
  { name: "XBRL Preview", href: "/xbrl-preview", icon: FileCode },
];

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center  ">
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="pr-0">
            <MobileNav pathname={pathname} setOpen={setOpen} />
          </SheetContent>
        </Sheet>
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <span className="font-bold text-xl">ESRS XBRL</span>
        </Link>
        <nav className="hidden md:flex md:flex-1 md:items-center md:justify-between">
          <div className="flex items-center space-x-4 lg:space-x-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  (
                    item.exact
                      ? pathname === item.href
                      : pathname.startsWith(item.href)
                  )
                    ? "text-primary"
                    : "text-muted-foreground"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>
          <div className="flex items-center space-x-4">
            <ModeToggle />
            <Button asChild>
              <Link href="/editor">Start Tagging</Link>
            </Button>
          </div>
        </nav>
        <div className="flex flex-1 items-center justify-end space-x-4 md:justify-end">
          <div className="hidden md:block">
            <ModeToggle />
          </div>
          <Button className="md:hidden" asChild>
            <Link href="/editor">Tag</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}

function MobileNav({
  pathname,
  setOpen,
}: {
  pathname: string;
  setOpen: (open: boolean) => void;
}) {
  return (
    <div className="flex flex-col space-y-4 py-4">
      <div className="flex items-center justify-between px-4">
        <Link
          href="/"
          className="flex items-center space-x-2"
          onClick={() => setOpen(false)}
        >
          <span className="font-bold text-xl">ESRS XBRL</span>
        </Link>
        <Button variant="ghost" size="icon" onClick={() => setOpen(false)}>
          <X className="h-5 w-5" />
          <span className="sr-only">Close</span>
        </Button>
      </div>
      <div className="px-2">
        <div className="flex flex-col space-y-1">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              onClick={() => setOpen(false)}
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                (
                  item.exact
                    ? pathname === item.href
                    : pathname.startsWith(item.href)
                )
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground"
              )}
            >
              {item.icon && <item.icon className="h-4 w-4" />}
              {item.name}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
