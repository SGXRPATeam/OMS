"use client";

import { useState } from "react";
import CreateOrderDrawer from "@/modules/dashboard/components/CreateOrderDrawer";
import AlertCards from "@/modules/dashboard/components/AlertCards";
import OrdersTable from "@/modules/dashboard/components/OrdersTable";
import { orders } from "@/mock/orders";
import {
  Package,
  Truck,
  Clock3,
  MessageSquare,
  Loader2,
  AlertTriangle,
  TrendingUp,
  Activity,
  Sparkles,
} from "lucide-react";

export default function DashboardPage() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const stats = [
    {
      title: "Total Orders",
      value: "2,847",
      icon: Package,
      color: "from-blue-500 to-indigo-600",
    },
    {
      title: "Active Orders",
      value: "1,243",
      icon: Truck,
      color: "from-emerald-500 to-green-600",
    },
    {
      title: "Delayed Orders",
      value: "47",
      icon: Clock3,
      color: "from-amber-500 to-orange-600",
    },
    {
      title: "Total Inquiries",
      value: "124",
      icon: MessageSquare,
      color: "from-violet-500 to-purple-600",
    },
    {
      title: "In Progress",
      value: "63",
      icon: Loader2,
      color: "from-cyan-500 to-sky-600",
    },
    {
      title: "Pending",
      value: "18",
      icon: AlertTriangle,
      color: "from-rose-500 to-pink-600",
    },
  ];

  const enquiries = [
    {
      id: "INQ-001",
      type: "Inquiry",
      category: "Order Status",
      priority: "High",
      assigned: "John",
      status: "Open",
      created: "2026-04-27",
    },
    {
      id: "CMP-002",
      type: "Complaint",
      category: "Late Delivery",
      priority: "Medium",
      assigned: "Alice",
      status: "In Progress",
      created: "2026-04-26",
    },
    {
      id: "DSP-003",
      type: "Dispute",
      category: "Payment",
      priority: "High",
      assigned: "Bob",
      status: "Pending",
      created: "2026-04-25",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Hero Header */}
      <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-primary to-indigo-700 text-white p-8 shadow-xl">
        <div className="flex flex-col lg:flex-row justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Sparkles size={18} />
              <span className="text-sm font-medium opacity-90">
                Enterprise OMS Dashboard
              </span>
            </div>

            <h1 className="text-4xl font-bold mb-3">
              Dashboard Overview
            </h1>

            <p className="text-white/80 max-w-2xl">
              Welcome back, John. Track orders, inquiries,
              escalations and operations in one place.
            </p>
          </div>

          <div className="flex flex-col items-start lg:items-end gap-4">
            <span className="text-sm text-white/80">
              Last updated: 5 mins ago
            </span>

            <button
              onClick={() => setOpenDrawer(true)}
              className="bg-white text-primary px-6 py-3 rounded-2xl font-semibold hover:scale-105 transition shadow-lg"
            >
              + Create Order
            </button>
          </div>
        </div>
      </div>

      {/* Quick Metrics */}
      {/* <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-white rounded-3xl p-5 border shadow-sm flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-blue-100 text-blue-600 flex items-center justify-center">
            <TrendingUp />
          </div>
          <div>
            <p className="text-sm text-gray-500">Growth</p>
            <h3 className="text-2xl font-bold">+18.4%</h3>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-5 border shadow-sm flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-green-100 text-green-600 flex items-center justify-center">
            <Activity />
          </div>
          <div>
            <p className="text-sm text-gray-500">System Health</p>
            <h3 className="text-2xl font-bold">98.9%</h3>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-5 border shadow-sm flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-violet-100 text-violet-600 flex items-center justify-center">
            <MessageSquare />
          </div>
          <div>
            <p className="text-sm text-gray-500">Response SLA</p>
            <h3 className="text-2xl font-bold">2.1 hrs</h3>
          </div>
        </div>
      </div> */}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {stats.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.title}
              className="group bg-white/80 backdrop-blur-lg rounded-3xl border border-white shadow-sm hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 p-6"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-sm text-gray-500 mb-2">
                    {item.title}
                  </p>

                  <h3 className="text-3xl font-bold text-gray-900">
                    {item.value}
                  </h3>
                </div>

                <div
                  className={`w-14 h-14 rounded-2xl bg-gradient-to-r ${item.color} text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition`}
                >
                  <Icon size={24} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Alerts */}
      <AlertCards />

      {/* Bottom Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="bg-white rounded-3xl border shadow-sm overflow-hidden">
          <OrdersTable data={orders.slice(0, 3)} />
        </div>

        <div className="bg-white rounded-3xl border shadow-sm p-6">
          <div className="flex justify-between items-start mb-5">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Recent Inquiries
              </h2>

              <p className="text-sm text-gray-500 mt-1">
                Track and manage latest inquiries
              </p>
            </div>

            <button className="text-primary text-sm font-medium hover:underline">
              View all
            </button>
          </div>

          <div className="space-y-4">
            {enquiries.map((item) => (
              <div
                key={item.id}
                className="rounded-2xl border p-4 hover:shadow-md transition"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-primary">
                      {item.id}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {item.category}
                    </p>
                  </div>

                  <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-medium">
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <CreateOrderDrawer
        open={openDrawer}
        onClose={() => setOpenDrawer(false)}
      />
    </div>
  );
}