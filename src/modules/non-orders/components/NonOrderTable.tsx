"use client";

import { useState } from "react";

const data = Array.from({ length: 26 }, (_, i) => ({
  id: `NOR-${100 + i}`,
  po: `PO-${200 + i}`,
  stock: `STK-${300 + i}`,
  date: "2026-04-29",
  status: "Pending",
}));

export default function NonOrderTable() {
  const [page, setPage] = useState(1);
  const perPage = 9;

  const start = (page - 1) * perPage;
  const end = start + perPage;

  const current = data.slice(start, end);
  const totalPages = Math.ceil(data.length / perPage);

  return (
    <div className="bg-white rounded-3xl border shadow-sm overflow-hidden">
      <div className="p-6 border-b">
        <h2 className="text-lg font-semibold">
          My Non Orders
        </h2>
      </div>

      <table className="w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="p-4 text-left">Non-Order ID</th>
            <th className="p-4 text-left">PO No</th>
            <th className="p-4 text-left">Stock No</th>
            <th className="p-4 text-left">Date</th>
            <th className="p-4 text-left">Status</th>
          </tr>
        </thead>

        <tbody>
          {current.map((item) => (
            <tr
              key={item.id}
              className="border-t hover:bg-gray-50"
            >
              <td className="p-4 text-primary font-medium">
                {item.id}
              </td>
              <td className="p-4">{item.po}</td>
              <td className="p-4">{item.stock}</td>
              <td className="p-4">{item.date}</td>
              <td className="p-4">{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="px-6 py-4 border-t flex justify-between items-center text-sm">
        <span>
          {start + 1}-{Math.min(end, data.length)} of {data.length}
        </span>

        <div className="flex gap-2">
          <button
            disabled={page === 1}
            onClick={() => setPage(page - 1)}
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            Prev
          </button>

          <button
            disabled={page === totalPages}
            onClick={() => setPage(page + 1)}
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}