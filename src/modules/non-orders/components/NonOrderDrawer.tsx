"use client";

import NonOrderForm from "./NonOrderForm";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function NonOrderDrawer({
  open,
  onClose,
}: Props) {
  return (
    <>
      <div
        onClick={onClose}
        className={`fixed inset-0 bg-black/30 z-40 transition ${
          open ? "opacity-100 visible" : "opacity-0 invisible"
        }`}
      />

      <div
        className={`fixed top-0 right-0 h-full w-[620px] bg-white z-50 shadow-2xl transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="sticky top-0 bg-primary text-white px-6 py-5 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">
              Submit New Non Order Request
            </h2>
            <p className="text-sm text-blue-100">
              Fill in the details below
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-3xl"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          <NonOrderForm />
        </div>
      </div>
    </>
  );
}