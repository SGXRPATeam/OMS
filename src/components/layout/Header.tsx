"use client";

import { useState } from "react";
import {
  Bell,
  Search,
  ChevronDown,
} from "lucide-react";
import {
  usePathname,
  useRouter,
} from "next/navigation";

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();

  const [open, setOpen] =
    useState(false);

  const showSearch =
    pathname === "/dashboard";

  const handleLogout = () => {
    localStorage.clear();
    router.push("/");
  };

  return (
    <header className="h-20 bg-white border-b px-8 flex items-center justify-between relative z-50">
      {/* Left */}
      <div className="flex items-center">
        {showSearch && (
          <div className="relative w-[420px]">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
            />

            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-11 pr-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        )}
      </div>

      {/* Right */}
      <div className="flex items-center gap-6">
        {/* Bell */}
        <div className="relative cursor-pointer">
          <Bell
            size={22}
            className="text-gray-600"
          />

          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse" />
        </div>

        {/* Profile */}
        <div className="relative">
          <div
            onClick={() =>
              setOpen(!open)
            }
            className="flex items-center gap-3 cursor-pointer"
          >
            <div className="w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center font-semibold text-lg">
              JD
            </div>

            <div className="leading-tight">
              <p className="font-medium text-gray-900">
                John Doe
              </p>
              <p className="text-sm text-gray-500">
                Admin
              </p>
            </div>

            <ChevronDown
              size={18}
              className={`transition ${
                open
                  ? "rotate-180"
                  : ""
              }`}
            />
          </div>

          {/* Dropdown */}
          {open && (
            <div className="absolute right-0 mt-4 w-60 bg-white rounded-2xl border shadow-xl overflow-hidden">
              <button
                onClick={() => {
                  setOpen(false);
                  router.push(
                    "/profile"
                  );
                }}
                className="w-full text-left px-5 py-4 hover:bg-gray-50"
              >
                My Profile
              </button>

              <button
                onClick={() => {
                  setOpen(false);
                  router.push(
                    "/users/register"
                  );
                }}
                className="w-full text-left px-5 py-4 hover:bg-gray-50"
              >
                Register User
              </button>

              <button
                onClick={handleLogout}
                className="w-full text-left px-5 py-4 hover:bg-red-50 text-red-500 border-t"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}