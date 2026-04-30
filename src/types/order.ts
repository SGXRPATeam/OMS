export type Order = {
  id: string;
  customer: string;
  orderType: "STD" | "NON-STD";
  amount: string;
  status: "Completed" | "Pending" | "Cancelled";
  progress: number;
  deliveryDate: string;
};