"use client";

import { useState } from "react";
import NonOrderDrawer from "@/modules/non-orders/components/NonOrderDrawer";
import NonOrderTable from "@/modules/non-orders/components/NonOrderTable";

export default function NonOrdersPage() {
  const [openDrawer, setOpenDrawer] = useState(false);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            My Non Orders
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Track and manage your non-order requests
          </p>
        </div>

        <button
          onClick={() => setOpenDrawer(true)}
          className="bg-primary text-white px-5 py-2.5 rounded-xl shadow-sm hover:opacity-90"
        >
          + New Non Order
        </button>
      </div>

      {/* List */}
      <NonOrderTable />

      {/* Drawer */}
      <NonOrderDrawer
        open={openDrawer}
        onClose={() => setOpenDrawer(false)}
      />
    </div>
  );
}