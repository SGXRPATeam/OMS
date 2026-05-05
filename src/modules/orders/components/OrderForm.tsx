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
    <form
      onSubmit={handleSubmit}
      className="space-y-5"
    >
      {/* Account Number */}
      <input
        value={form.account_number}
        placeholder="Account Number"
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
        onChange={(e) =>
          setForm({
            ...form,
            account_number: e.target.value,
          })
        }
      />

      {/* Product */}
      <input
        value={form.product}
        placeholder="Product"
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
        onChange={(e) =>
          setForm({
            ...form,
            product: e.target.value,
          })
        }
      />

      {/* Quantity */}
      <input
        value={form.quantity}
        placeholder="Quantity"
        type="number"
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
        onChange={(e) =>
          setForm({
            ...form,
            quantity: e.target.value,
          })
        }
      />

      {/* Description */}
      <textarea
        value={form.description}
        placeholder="Description"
        rows={4}
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary resize-none"
        onChange={(e) =>
          setForm({
            ...form,
            description: e.target.value,
          })
        }
      />

      {/* Delivery Address */}
      <textarea
        value={form.delivery_address}
        placeholder="Delivery Address"
        rows={3}
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary resize-none"
        onChange={(e) =>
          setForm({
            ...form,
            delivery_address: e.target.value,
          })
        }
      />

      {/* Order Type */}
      <select
        value={form.order_type}
        className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
        onChange={(e) =>
          setForm({
            ...form,
            order_type: e.target.value,
          })
        }
      >
        <option value="STANDARD">
          Standard
        </option>

        <option value="NON_STANDARD">
          Non Standard
        </option>
      </select>

      {/* Button */}
      <button
        type="submit"
        className="w-full bg-primary text-white py-3 rounded-xl font-medium hover:opacity-90 transition"
      >
        Submit Order
      </button>
    </form>
  );
}