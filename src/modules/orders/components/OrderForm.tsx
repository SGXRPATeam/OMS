"use client";

import { useState } from "react";
import { OrderService } from "@/services/order.service";

export default function OrderForm() {
  const [form, setForm] = useState({
    account_number: "",
    product: "",
    quantity: "",
    description: "",
    delivery_address: "",
    order_type: "STANDARD",
  });

  // REPLACE ONLY THIS FUNCTION
  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (
      !form.account_number ||
      !form.product ||
      !form.quantity ||
      !form.description ||
      !form.delivery_address
    ) {
      alert("Please fill all fields");
      return;
    }

    await OrderService.create({
      ...form,
      quantity: Number(form.quantity),
    });

    alert("Order created successfully");

    setForm({
      account_number: "",
      product: "",
      quantity: "",
      description: "",
      delivery_address: "",
      order_type: "STANDARD",
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* remaining code same */}
    </form>
  );
}