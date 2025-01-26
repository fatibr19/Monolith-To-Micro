import "./globals.css";
import type { Metadata } from "next";
import localFont from 'next/font/local'


import Header from "@/components/Header/header";

export const metadata: Metadata = {
  title: "Decomposition des Monolithes",
  description: "le bute est de faciliter la décomposition des monolithes en microservices",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>
        <Header/>

        {children}
        
        </body>
    </html>
  );
}
