"use client";

import { useState } from "react";
import InquiryCards from "@/modules/inquiries/components/InquiryCards";
import InquiryForm from "@/modules/inquiries/components/InquiryForm";
import InquiryList from "@/modules/inquiries/components/InquiryList";
import { Search } from "lucide-react";

import type {
  Inquiry,
  InquiryType,
} from "@/types/inquiry";

import { inquiries as initialInquiries } from "@/mock/inquiries";

export default function InquiriesPage() {

  

  const [activeType, setActiveType] =
    useState<InquiryType | null>(null);

  const [search, setSearch] = useState("");
  const [listFilter, setListFilter] = useState("all");

  const [inquiryList, setInquiryList] =
    useState<Inquiry[]>(initialInquiries);

  const filteredInquiries = inquiryList.filter((item) => {
  const matchesType =
    listFilter === "all"
      ? true
      : item.type.toLowerCase() === listFilter;

  const matchesSearch = item.id
    .toLowerCase()
    .includes(search.toLowerCase());

  return matchesType && matchesSearch;
});

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
    {/* Search + Filter */}
<div className="flex flex-col md:flex-row gap-4 justify-between items-center">
  {/* Search */}
  <div className="relative w-full md:w-80">
  <Search
    size={18}
    className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
  />

  <input
    type="text"
    placeholder="Search by ID..."
    value={search}
    onChange={(e) => setSearch(e.target.value)}
    className="w-full border rounded-xl pl-11 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
  />
</div>

  {/* Filter */}
  <select
    value={listFilter}
    onChange={(e) => setListFilter(e.target.value)}
    className="w-full md:w-56 border rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
  >
    <option value="all">All</option>
    <option value="inquiry">Inquiry</option>
    <option value="complaint">Complaint</option>
    <option value="dispute">Dispute</option>
  </select>
</div>

{/* List */}
<InquiryList data={filteredInquiries} />
    </div>
  );
}