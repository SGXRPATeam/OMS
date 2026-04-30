"use client";

import { useState } from "react";
import InquiryCards from "@/modules/inquiries/components/InquiryCards";
import InquiryForm from "@/modules/inquiries/components/InquiryForm";
import InquiryList from "@/modules/inquiries/components/InquiryList";

import type {
  Inquiry,
  InquiryType,
} from "@/types/inquiry";

import { inquiries as initialInquiries } from "@/mock/inquiries";

export default function InquiriesPage() {

  

  const [activeType, setActiveType] =
    useState<InquiryType | null>(null);

  const [search, setSearch] = useState("");

  const [inquiryList, setInquiryList] =
    useState<Inquiry[]>(initialInquiries);

  const filteredInquiries = inquiryList.filter((item) =>
  [
    item.id,
    item.type,
    item.category,
    item.description,
    item.status,
  ]
    .join(" ")
    .toLowerCase()
    .includes(search.toLowerCase())
);  

  const handleAddInquiry = (
    category: string,
    description: string
  ) => {
    if (!activeType) return;

    const prefix =
      activeType === "complaint"
        ? "CMP"
        : activeType === "inquiry"
        ? "INQ"
        : "DSP";

    const newItem: Inquiry = {
      id: `${prefix}-${String(inquiryList.length + 1).padStart(3, "0")}`,
      type: activeType,
      category,
      description,
      status: "Open",
      createdAt: new Date().toISOString().split("T")[0],
    };

    setInquiryList((prev) => [newItem, ...prev]);
  };

  return (
    <div className="space-y-8">
      {/* Heading */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Inquiries & Support
        </h1>

        <p className="text-gray-500 mt-2">
          Manage complaints, inquiries, and disputes efficiently
        </p>
      </div>


      {/* Cards */}
      <InquiryCards
        activeType={activeType}
        setActiveType={setActiveType}
      />

      {/* Form */}
      {activeType && (
  <div className="bg-white rounded-2xl border shadow-sm p-6">
    {/* Header */}
    <div className="flex justify-between items-center border-b pb-4">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">
          {activeType === "complaint" && "Raise Complaint"}
          {activeType === "inquiry" && "Submit Inquiry"}
          {activeType === "dispute" && "Raise Dispute"}
        </h2>

        <p className="text-sm text-gray-500 mt-1">
          Fill the details below
        </p>
      </div>

      {/* Back Button */}
      <button
        onClick={() => setActiveType(null)}
        className="text-primary text-sm font-medium hover:underline"
      >
        ← Back to options
      </button>
    </div>

    {/* Form */}
    <div className="mt-6">
      <InquiryForm
        type={activeType}
        onSubmit={handleAddInquiry}
      />
    </div>
  </div>
)}

      {/* List */}
      <InquiryList data={filteredInquiries} />
    </div>
  );
}