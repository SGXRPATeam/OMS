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
} from "lucide-react";

export default function DashboardPage() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const stats = [
    {
      title: "Total Orders",
      value: "2,847",
      icon: Package,
      color: "from-blue-500 to-indigo-500",
    },
    {
      title: "Active Orders",
      value: "1,243",
      icon: Truck,
      color: "from-emerald-500 to-green-500",
    },
    {
      title: "Delayed Orders",
      value: "47",
      icon: Clock3,
      color: "from-amber-500 to-orange-500",
    },
    {
      title: "Total Inquiries",
      value: "124",
      icon: MessageSquare,
      color: "from-violet-500 to-purple-500",
    },
    {
      title: "In Progress",
      value: "63",
      icon: Loader2,
      color: "from-cyan-500 to-sky-500",
    },
    {
      title: "Pending",
      value: "18",
      icon: AlertTriangle,
      color: "from-rose-500 to-pink-500",
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
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Dashboard Overview
        </h1>

        <p className="text-sm text-gray-500 mt-2">
          Welcome back, John! Here's what's happening with your orders today.
        </p>
      </div>

      {/* Top Action */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">
          Last updated: 5 mins ago
        </p>

        <button
          onClick={() => setOpenDrawer(true)}
          className="bg-primary hover:opacity-90 transition text-white px-5 py-2.5 rounded-xl text-sm font-medium shadow-sm"
        >
          + Create Order
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {stats.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.title}
              className="bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 p-6"
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
                  className={`w-14 h-14 rounded-2xl bg-gradient-to-r ${item.color} text-white flex items-center justify-center shadow-md`}
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

      {/* Bottom Split */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Recent Orders */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
          <OrdersTable data={orders.slice(0, 3)} />
        </div>

        {/* Recent Enquiries */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6">
          <div className="flex justify-between items-start mb-5">
  <div>
    <h2 className="text-lg font-semibold text-gray-900">
      Recent Enquiries
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      Track and manage your latest inquiry
    </p>
  </div>

  <button className="text-primary text-sm font-medium hover:underline">
    View all
  </button>
</div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-3">ID</th>
                  <th className="pb-3">Type</th>
                  <th className="pb-3">Category</th>
                  <th className="pb-3">Priority</th>
                  <th className="pb-3">Assigned</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Created</th>
                  <th className="pb-3 text-center">
                    Action
                  </th>
                </tr>
              </thead>

              <tbody>
                {enquiries.map((item) => (
                  <tr
                    key={item.id}
                    className="border-b last:border-none hover:bg-gray-50 transition"
                  >
                    <td className="py-4 font-medium text-primary">
                      {item.id}
                    </td>

                    <td className="py-4">
                      {item.type}
                    </td>

                    <td className="py-4">
                      {item.category}
                    </td>

                    <td className="py-4">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          item.priority === "High"
                            ? "bg-red-100 text-red-600"
                            : item.priority === "Medium"
                            ? "bg-yellow-100 text-yellow-600"
                            : "bg-green-100 text-green-600"
                        }`}
                      >
                        {item.priority}
                      </span>
                    </td>

                    <td className="py-4">
                      {item.assigned}
                    </td>

                    <td className="py-4">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          item.status === "Resolved"
                            ? "bg-green-100 text-green-600"
                            : item.status === "In Progress"
                            ? "bg-yellow-100 text-yellow-600"
                            : item.status === "Pending"
                            ? "bg-orange-100 text-orange-600"
                            : "bg-blue-100 text-blue-600"
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>

                    <td className="py-4 text-gray-500">
                      {item.created}
                    </td>

                    <td className="py-4 text-center text-lg cursor-pointer">
                      ⋮
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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