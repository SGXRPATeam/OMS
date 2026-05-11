"use client";

export default function NonOrderForm() {
  return (
    <form className="space-y-5">
      <div>
        <label className="block mb-2 text-sm font-medium">
          Account Number
        </label>
        <input
          className="w-full border rounded-xl px-4 py-3"
          placeholder="Enter account number"
        />
      </div>

      <div>
        <label className="block mb-2 text-sm font-medium">
          Product
        </label>
        <input
          className="w-full border rounded-xl px-4 py-3"
          placeholder="Enter product"
        />
      </div>

      <div>
        <label className="block mb-2 text-sm font-medium">
          Quantity
        </label>
        <input
          type="number"
          className="w-full border rounded-xl px-4 py-3"
          placeholder="Enter quantity"
        />
      </div>

      <div>
        <label className="block mb-2 text-sm font-medium">
          Description
        </label>
        <textarea
          rows={4}
          className="w-full border rounded-xl px-4 py-3"
          placeholder="Enter description"
        />
      </div>

      <div>
        <label className="block mb-2 text-sm font-medium">
          Delivery Address
        </label>
        <textarea
          rows={3}
          className="w-full border rounded-xl px-4 py-3"
          placeholder="Enter delivery address"
        />
      </div>

      <button className="w-full bg-primary text-white py-3 rounded-xl font-medium">
        Submit
      </button>
    </form>
  );
}