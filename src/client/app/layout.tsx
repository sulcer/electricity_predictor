import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "@/components/providers/providers";
import {ReactNode, Suspense} from "react";
import LoadingSpinner from "@/components/ui/loading-spinner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Electricity predictor",
  description: "Electricity predictor project",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
      <html lang="en">
      <body className={inter.className}>
      <Providers>
        <Suspense fallback={
          <div className={'self-center my-auto'}>
            <LoadingSpinner className={'w-8 h-8'}/>
          </div>}
        >
          {children}
        </Suspense>
      </Providers>
      </body>
      </html>
  );
}
