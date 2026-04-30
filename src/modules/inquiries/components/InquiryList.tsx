import type { Inquiry } from "@/types/inquiry";

type Props = {
  data: Inquiry[];
};

export default function InquiryList({ data }: Props) {
  return (
    <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-5 border-b">
        <h2 className="text-xl font-semibold text-gray-900">
          Inquiry List
        </h2>

        <p className="text-sm text-gray-500 mt-1">
          Track all complaints, inquiries, and disputes
        </p>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full table-fixed text-sm">
          <thead className="bg-gray-50 border-b">
            <tr className="text-left text-textSecondary">
              <th className="w-[14%] px-6 py-4">ID</th>
              <th className="w-[14%] px-6 py-4">Type</th>
              <th className="w-[18%] px-6 py-4">Category</th>
              <th className="w-[26%] px-6 py-4">Description</th>
              <th className="w-[12%] px-6 py-4">Status</th>
              <th className="w-[12%] px-6 py-4">Created</th>
              <th className="w-[4%] px-6 py-4 text-center">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
  {data.length === 0 ? (
    <tr>
      <td
        colSpan={7}
        className="text-center py-10 text-gray-500"
      >
        No records found
      </td>
    </tr>
  ) : (
    data.map((item) => (
      <tr
        key={item.id}
        className="border-b last:border-none hover:bg-gray-50"
      >
        <td className="px-6 py-5 font-medium text-primary">
          {item.id}
        </td>

        <td className="px-6 py-5 capitalize">
          {item.type}
        </td>

        <td className="px-6 py-5">
          {item.category}
        </td>

        <td className="px-6 py-5 truncate">
          {item.description}
        </td>

        <td className="px-6 py-5">
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${
              item.status === "Resolved"
                ? "bg-green-100 text-green-600"
                : item.status === "In Progress"
                ? "bg-yellow-100 text-yellow-600"
                : "bg-blue-100 text-blue-600"
            }`}
          >
            {item.status}
          </span>
        </td>

        <td className="px-6 py-5 text-gray-500">
          {item.createdAt}
        </td>

        <td className="px-6 py-5 text-center">
          ⋮
        </td>
      </tr>
    ))
  )}
</tbody>
        </table>
      </div>
    </div>
  );
}