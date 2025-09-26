export const metadata = {
  title: "Todo App",
  description: "Class project scaffold",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ padding: 24 }}>{children}</body>
    </html>
  );
}
