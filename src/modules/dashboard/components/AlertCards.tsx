import { AlertCircle, Clock, AlertTriangle, Sparkles } from "lucide-react";

export default function AlertCards() {
  return (
    <div className="space-y-4">

      <div className="flex justify-between items-center">
  <div className="flex items-center gap-3">
    <div className="flex items-center gap-2 mb-5">
  <AlertTriangle size={22} className="text-indigo-600" />

  <h2 className="text-3xl font-semibold text-textPrimary tracking-tight">
    Alerts
  </h2>


    {/* AI Powered Badge */}
    <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xs font-medium shadow-sm">
  <Sparkles size={14} className="fill-white animate-sparkle" />
  <span>AI Powered</span>
</div>
  </div>
  </div>

  {/* <button className="text-primary text-sm font-medium hover:underline">
    View all alerts →
  </button> */}
</div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Card 1 */}
        <div className="border rounded-xl p-4 bg-red-50">
          <div className="flex justify-between items-center">
            <AlertCircle className="text-red-500" />
            <span className="bg-red-500 text-white text-xs px-2 py-1 rounded">
              15
            </span>
          </div>
          <h3 className="mt-3 font-semibold">Delayed Shipments</h3>
          <p className="text-sm text-gray-600">
            15 orders are at risk of missing delivery deadlines.
          </p>
          <p className="text-red-500 text-sm mt-2 cursor-pointer">
            View Details →
          </p>
        </div>

        {/* Card 2 */}
        <div className="border rounded-xl p-4 bg-orange-50">
          <div className="flex justify-between items-center">
            <Clock className="text-orange-500" />
            <span className="bg-orange-500 text-white text-xs px-2 py-1 rounded">
              8
            </span>
          </div>
          <h3 className="mt-3 font-semibold">Pending Approvals</h3>
          <p className="text-sm text-gray-600">
            Orders require approval to proceed.
          </p>
          <p className="text-orange-500 text-sm mt-2 cursor-pointer">
            View Details →
          </p>
        </div>

        {/* Card 3 */}
        <div className="border rounded-xl p-4 bg-yellow-50">
          <div className="flex justify-between items-center">
            <AlertTriangle className="text-yellow-500" />
            <span className="bg-yellow-500 text-white text-xs px-2 py-1 rounded">
              12
            </span>
          </div>
          <h3 className="mt-3 font-semibold">Low Stock Alert</h3>
          <p className="text-sm text-gray-600">
            Products running low on inventory.
          </p>
          <p className="text-yellow-500 text-sm mt-2 cursor-pointer">
            View Details →
          </p>
        </div>

      </div>
    </div>
  );
}