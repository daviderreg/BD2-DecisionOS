import './globals.css'; // <--- QUESTO È IL PUNTO CHIAVE: Importa i CSS di Tailwind
import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'DecisionOS',
  description: 'Corporate Memory & RAG Intelligence',
};

export default function RootLayout({ children }) {
  return (
    <html lang="it">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}