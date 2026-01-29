import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AppProvider } from "../context/AppContext";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"]
});

export const metadata: Metadata = {
  title: "LearnFlow - AI-Powered Python Tutoring",
  description: "An intelligent Python tutoring platform with AI agents for personalized learning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} antialiased`}
      >
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  );
}
