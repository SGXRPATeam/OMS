"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "@/constants/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 h-screen bg-white border-r flex flex-col justify-between">
      
      {/* Top Section */}
      <div>
        {/* Logo */}
        <div className="p-6 text-xl font-bold text-primary">
          Enterprise OMS
        </div>

        {/* Navigation */}
        <nav className="px-3 space-y-2">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.path;
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.path}
                className={`flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition
                  ${
                    isActive
                      ? "bg-primary text-white"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
              >
                <Icon  size={20}/>
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="p-4">
        <button className="text-red-500 text-sm font-medium">
          Logout
        </button>
      </div>
    </aside>
  );
}