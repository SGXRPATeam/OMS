"use client";

import { useMemo, useState } from "react";
import { Search } from "lucide-react";
import InquiryList from "@/modules/inquiries/components/InquiryList";
import { inquiries } from "@/mock/inquiries";

export default function DisputesPage() {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [page, setPage] = useState(1);

  const pageSize = 9;

  // only disputes
  const disputeData = inquiries.filter(
    (item) => item.type === "dispute"
  );

  // fixed dispute types
  const disputeTypes = [
    "all",
    "Invoice",
    "Delivery",
    "Quality",
    "Refund",
    "Other",
  ];

  // filter + search
  const filteredData = disputeData.filter((item) => {
    const matchesSearch = item.id
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesFilter =
      filter === "all"
        ? true
        : item.category === filter;

    return matchesSearch && matchesFilter;
  });

  // pagination
  const total = filteredData.length;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;

  const paginatedData = useMemo(
    () => filteredData.slice(start, end),
    [filteredData, start, end]
  );

  return (
    <div className="space-y-6">
      {/* Heading */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Dispute List
        </h1>

        <p className="text-gray-500 mt-1">
          Manage all disputes efficiently
        </p>
      </div>

      {/* Search + Filter */}
      <div className="flex flex-col md:flex-row gap-4 justify-between">
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
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="w-full border rounded-xl pl-11 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Filter */}
        <select
          value={filter}
          onChange={(e) => {
            setFilter(e.target.value);
            setPage(1);
          }}
          className="w-full md:w-64 border rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {disputeTypes.map((type) => (
            <option key={type} value={type}>
              {type === "all"
                ? "All Dispute Types"
                : type}
            </option>
          ))}
        </select>
      </div>

      {/* List */}
      <InquiryList data={paginatedData} />

      {/* Pagination */}
      <div className="flex justify-between items-center text-sm text-gray-500 border-t pt-4">
        <p>
          {total === 0 ? 0 : start + 1}–{Math.min(end, total)} of {total}
        </p>

        <div className="flex gap-2">
          <button
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
            className="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-50"
          >
            Prev
          </button>

          <button
            disabled={end >= total}
            onClick={() => setPage((p) => p + 1)}
            className="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}