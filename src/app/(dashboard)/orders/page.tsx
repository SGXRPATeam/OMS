"use client";

import { useEffect, useState } from "react";
import OrdersTable from "@/modules/dashboard/components/OrdersTable";
import OrderFilters from "@/modules/orders/components/OrderFilters";
import CreateOrderDrawer from "@/modules/dashboard/components/CreateOrderDrawer";
import { OrderService } from "@/services/order.service";

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [openDrawer, setOpenDrawer] = useState(false);

  // Fetch from backend
  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const data = await OrderService.getAll();

      const formatted = data.map((item: any) => ({
  id: item.caseid,
  customer: item.account_number,
  type: item.order_type,
  status: item.status,
  deliveryDate: item.delivery_date,
  amount: item.quantity,
  progress: 100,
}));

      setOrders(formatted);
    } catch (error) {
      console.error("Failed to fetch orders", error);
    }
  };

  // Filter
  const filteredOrders = orders.filter((order) => {
    const matchesSearch =
      order.id
        ?.toLowerCase()
        .includes(search.toLowerCase()) ||
      order.customer
        ?.toLowerCase()
        .includes(search.toLowerCase());

    const matchesStatus = status
      ? order.status === status
      : true;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">
          Orders
        </h1>

        <button
          onClick={() => setOpenDrawer(true)}
          className="bg-primary text-white px-4 py-2 rounded-lg text-sm"
        >
          + Create Order
        </button>
      </div>

      {/* Filters */}
      <OrderFilters
        search={search}
        setSearch={setSearch}
        status={status}
        setStatus={setStatus}
      />

      {/* Table */}
      <OrdersTable data={filteredOrders} />

      {/* Drawer */}
      <CreateOrderDrawer
        open={openDrawer}
        onClose={() => {
          setOpenDrawer(false);
          fetchOrders(); // refresh table
        }}
      />
    </div>
  );
}