"use client";

import Sidebar from "./Sidebar";
import Header from "./Header";
import FloatingChatButton from "@/modules/ai/components/FloatingChatButton";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      {/* Fixed Sidebar */}
      <aside className="w-64 shrink-0 h-screen border-r bg-white fixed left-0 top-0 z-40">
        <Sidebar />
      </aside>

      {/* Main */}
      <div className="flex-1 ml-64 flex flex-col h-screen overflow-hidden">
        {/* Fixed Header */}
        <div className="shrink-0 bg-white border-b sticky top-0 z-30">
          <Header />
        </div>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>

      {/* Floating AI Chat */}
      <div className="fixed bottom-6 right-6 z-50">
        <FloatingChatButton />
      </div>
    </div>
  );
}