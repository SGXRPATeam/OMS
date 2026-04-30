import type { Order } from "@/types/order";

export const orders: Order[] = [
 {
  id: "ORD001",
  customer: "John Doe",
  orderType: "STD",
  status: "Completed",
  deliveryDate: "2024-06-15",
  amount: "$120",
  progress: 100,
},
{
  id: "ORD002",
  customer: "Alice Smith",
  orderType: "NON-STD",
  status: "Pending",
  deliveryDate: "2024-06-18",
  amount: "$80",
  progress: 65,
},
{
  id: "ORD003",
  customer: "Bob Johnson",
  orderType: "STD",
  status: "Cancelled",
  deliveryDate: "2024-06-22",
  amount: "$250",
  progress: 30,
},
];