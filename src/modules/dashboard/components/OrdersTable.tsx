import { orders } from "@/mock/orders";
type Order = {
  id: string;
  customer: string;
  orderType: "STD" | "NON-STD";
  amount: string;
  status: string;
  deliveryDate: string;
  progress: number;
};

export default function OrdersTable({ data }: { data: Order[] }) {
  return (
    <div className="bg-card rounded-xl border shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center px-6 py-5 border-b">
        <div>
          <h2 className="text-lg font-semibold">Recent Orders</h2>
          <p className="text-sm text-gray-500">
            Track and manage your latest orders
          </p>
        </div>

        <button className="text-primary text-sm font-medium hover:underline">
          View all orders →
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full table-fixed text-sm">
          <thead className="bg-gray-50 border-b">
            <tr className="text-left text-textSecondary">
              <th className="w-[12%] px-6 py-4 font-medium">Order ID</th>
              <th className="w-[18%] px-6 py-4 font-medium">Customer</th>
              <th className="w-[12%] px-6 py-4 font-medium">Order Type</th>
              <th className="w-[14%] px-6 py-4 font-medium">Status</th>
              <th className="w-[14%] px-6 py-4 font-medium">
                Delivery Date
              </th>
              <th className="w-[8%] px-6 py-4 font-medium">Amount</th>
              
              <th className="w-[18%] px-6 py-4 font-medium">Progress</th>
              <th className="w-[4%] px-6 py-4 text-center font-medium">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            {data.map((order) => (
              <tr
                key={order.id}
                className="border-b last:border-none hover:bg-gray-50 transition"
              >
                {/* Order ID */}
                <td className="px-6 py-5 font-medium text-primary">
                  {order.id}
                </td>

                {/* Customer */}
                <td className="px-6 py-5">{order.customer}</td>

                {/* Order Type */}
                <td className="px-6 py-5">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      order.orderType === "STD"
                        ? "bg-blue-100 text-blue-600"
                        : "bg-purple-100 text-purple-600"
                    }`}
                  >
                    {order.orderType}
                  </span>
                </td>

                {/* Status */}
                <td className="px-6 py-5">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      order.status === "Completed"
                        ? "bg-green-100 text-green-600"
                        : order.status === "Pending"
                        ? "bg-yellow-100 text-yellow-600"
                        : "bg-red-100 text-red-600"
                    }`}
                  >
                    {order.status}
                  </span>
                </td>

                

                {/* Delivery Date */}
                <td className="px-6 py-5 text-gray-600">
                  {order.deliveryDate}
                </td>

                {/* Amount */}
                <td className="px-6 py-5 font-semibold">
                  {order.amount}
                </td>

                {/* Progress */}
                <td className="px-6 py-5">
                  <div className="flex items-center gap-3">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          order.status === "Completed"
                            ? "bg-green-500"
                            : order.status === "Pending"
                            ? "bg-blue-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${order.progress}%` }}
                      />
                    </div>

                    <span className="text-xs text-gray-500 min-w-[40px]">
                      {order.progress}%
                    </span>
                  </div>
                </td>

                {/* Actions */}
                <td className="px-6 py-5 text-center">
                  <button className="text-gray-500 hover:text-primary text-lg">
                    ⋮
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}