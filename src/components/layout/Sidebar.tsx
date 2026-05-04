"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "@/constants/navigation";
import { ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

function SidebarItem({
  item,
  level = 0,
}: {
  item: any;
  level?: number;
}) {
  const pathname = usePathname();
  const [open, setOpen] = useState(true);

  const Icon = item.icon;

  // Dropdown menu
  if (item.children) {
    return (
      <div>
        <button
          onClick={() => setOpen(!open)}
          className="w-full flex items-center justify-between px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition"
          style={{ paddingLeft: `${16 + level * 18}px` }}
        >
          <div className="flex items-center gap-3">
            <Icon size={20} />
            {item.name}
          </div>

          {open ? (
            <ChevronDown size={16} />
          ) : (
            <ChevronRight size={16} />
          )}
        </button>

        {open && (
          <div className="mt-1 space-y-1">
            {item.children.map((child: any) => (
              <SidebarItem
                key={child.name}
                item={child}
                level={level + 1}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  // Normal link
  const isActive = pathname === item.path;

  return (
    <Link
      href={item.path}
      className={`flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition ${
        isActive
          ? "bg-primary text-white"
          : "text-gray-600 hover:bg-gray-100"
      }`}
      style={{ paddingLeft: `${16 + level * 18}px` }}
    >
      <Icon size={20} />
      {item.name}
    </Link>
  );
}

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-white border-r flex flex-col justify-between">
      {/* Top */}
      <div>
        <div className="p-6 text-xl font-bold text-primary">
          Enterprise OMS
        </div>

        <nav className="px-3 space-y-2">
          {NAV_ITEMS.map((item) => (
            <SidebarItem
              key={item.name}
              item={item}
            />
          ))}
        </nav>
      </div>

      {/* Bottom */}
      <div className="p-4">
        <button className="text-red-500 text-sm font-bold hover:text-red-700">
          Logout
        </button>
      </div>
    </aside>
  );
}