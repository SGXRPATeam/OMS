type Props = {
  title: string;
  value: string;
};

export default function StatCard({ title, value }: Props) {
  return (
    <div className="bg-card p-5 rounded-xl shadow-sm border">
      <p className="text-sm text-textSecondary">{title}</p>
      <h2 className="text-2xl font-semibold mt-2 text-textPrimary">
        {value}
      </h2>
    </div>
  );
}

// import { ShoppingCart, TrendingUp, Clock, MessageSquare } from "lucide-react";

// const icons = {
//   orders: { icon: ShoppingCart, bg: "bg-blue-100", color: "text-blue-600" },
//   revenue: { icon: TrendingUp, bg: "bg-green-100", color: "text-green-600" },
//   pending: { icon: Clock, bg: "bg-red-100", color: "text-red-500" },
//   completed: { icon: MessageSquare, bg: "bg-yellow-100", color: "text-yellow-600" },
// };

// export default function StatCard({ title, value, type, trend }: any) {
//   const Icon = icons[type].icon;

//   return (
//     <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex justify-between items-center">

//       <div>
//         <p className="text-sm text-gray-500">{title}</p>

//         <h2 className="text-2xl font-semibold mt-1">{value}</h2>

//         {trend && (
//           <span className={`text-xs mt-2 inline-block px-2 py-1 rounded-full ${
//             trend.type === "up"
//               ? "bg-green-100 text-green-600"
//               : "bg-red-100 text-red-600"
//           }`}>
//             {trend.text}
//           </span>
//         )}
//       </div>

//       <div className={`w-10 h-10 flex items-center justify-center rounded-lg ${icons[type].bg}`}>
//         <Icon className={icons[type].color} size={18} />
//       </div>

//     </div>
//   );
// }