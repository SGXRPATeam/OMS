"use client";

import OrderForm from "@/modules/orders/components/OrderForm";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function CreateOrderDrawer({ open, onClose }: Props) {
  return (
    <>
      {/* Overlay */}
      <div
        onClick={onClose}
        className={`fixed inset-0 bg-black/30 z-40 transition-opacity ${
          open ? "opacity-100 visible" : "opacity-0 invisible"
        }`}
      />

      {/* Drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-[520px] bg-white z-50 shadow-2xl transition-transform duration-300 overflow-y-auto ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="sticky top-0 bg-primary text-white px-6 py-5 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">Submit New Order Request</h2>
            <p className="text-sm text-blue-100">
              Fill in the details below
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-2xl hover:opacity-80"
          >
            ×
          </button>
        </div>

        {/* Form */}
        <div className="p-6">
          <OrderForm />
        </div>
      </div>
    </>
  );
}