import { AuthProvider } from "@/hooks/useAuth";
import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ESRS XBRL Tagging Platform",
  description:
    "A comprehensive solution for tagging financial reports with ESRS XBRL concepts",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <Toaster richColors position="top-right" />
          <div className="relative flex min-h-screen flex-col">{children}</div>
        </AuthProvider>
      </body>
    </html>
  );
}
