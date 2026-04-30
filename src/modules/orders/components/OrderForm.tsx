"use client";

import { useState } from "react";

type FormData = {
  accountNumber: string;
  product: string;
  orderType: string;
  quantity: string;
  description: string;
  deliveryAddress: string;
};

type Errors = Partial<FormData>;

export default function OrderForm() {
  const [form, setForm] = useState<FormData>({
    accountNumber: "",
    product: "",
    orderType: "",
    quantity: "",
    description: "",
    deliveryAddress: "",
  });

  const [errors, setErrors] = useState<Errors>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));

    // clear error while typing
    setErrors((prev) => ({
      ...prev,
      [e.target.name]: "",
    }));
  };

  const validate = () => {
    const newErrors: Errors = {};

    if (!form.accountNumber.trim()) {
      newErrors.accountNumber = "Account Number is required";
    }

    if (!form.product.trim()) {
      newErrors.product = "Product is required";
    }

    if (!form.orderType.trim()) {
      newErrors.orderType = "Order Type is required";
    }

    if (!form.quantity.trim()) {
      newErrors.quantity = "Quantity is required";
    } else if (Number(form.quantity) <= 0) {
      newErrors.quantity = "Quantity must be greater than 0";
    }

    if (!form.description.trim()) {
      newErrors.description = "Description is required";
    }

    if (!form.deliveryAddress.trim()) {
      newErrors.deliveryAddress = "Delivery Address is required";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

 const handleSubmit = () => {
  if (!validate()) return;

  console.log("Submitted:", form);
  alert("Order Submitted Successfully");

  // reset form
  setForm({
    accountNumber: "",
    product: "",
    orderType: "",
    quantity: "",
    description: "",
    deliveryAddress: "",
  });

  // clear validation errors
  setErrors({});
};

  return (
    <form className="space-y-6">
      {/* Heading */}
      <h2 className="text-xl font-semibold text-gray-800 border-b pb-4">
        Submit New Order Request
      </h2>

      {/* Fields */}
      <div className="space-y-5">
        {/* Account Number */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Account Number
          </label>
          <input
            name="accountNumber"
            value={form.accountNumber}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2"
          />
          {errors.accountNumber && (
            <p className="text-red-500 text-sm mt-1">
              {errors.accountNumber}
            </p>
          )}
        </div>

        {/* Product */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Product
          </label>
          <input
            name="product"
            value={form.product}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2"
          />
          {errors.product && (
            <p className="text-red-500 text-sm mt-1">
              {errors.product}
            </p>
          )}
        </div>

        {/* Order Type */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Order Type
          </label>
          <select
            name="orderType"
            value={form.orderType}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2 bg-white"
          >
            <option value="">Select Order Type</option>
            <option value="Standard Order">Standard Order</option>
            <option value="Non Standard Order">Non Standard Order</option>
          </select>
          {errors.orderType && (
            <p className="text-red-500 text-sm mt-1">
              {errors.orderType}
            </p>
          )}
        </div>

        {/* Quantity */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Quantity
          </label>
          <input
            type="number"
            name="quantity"
            value={form.quantity}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2"
          />
          {errors.quantity && (
            <p className="text-red-500 text-sm mt-1">
              {errors.quantity}
            </p>
          )}
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Description
          </label>
          <input
            name="description"
            value={form.description}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2"
          />
          {errors.description && (
            <p className="text-red-500 text-sm mt-1">
              {errors.description}
            </p>
          )}
        </div>

        {/* Delivery Address */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Delivery Address
          </label>
          <input
            name="deliveryAddress"
            value={form.deliveryAddress}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-2"
          />
          {errors.deliveryAddress && (
            <p className="text-red-500 text-sm mt-1">
              {errors.deliveryAddress}
            </p>
          )}
        </div>
      </div>

      {/* Submit */}
      <div className="flex justify-end">
        <button
          type="button"
          onClick={handleSubmit}
          className="bg-primary text-white px-6 py-2 rounded-lg"
        >
          Submit
        </button>
      </div>
    </form>
  );
}