import { z } from "zod";

export const orderSchema = z.object({
  customer: z.string().min(2, "Customer name is required"),
  product: z.string().min(2, "Product is required"),
  amount: z.string().min(1, "Amount is required"),
  status: z.enum(["Pending", "Completed", "Cancelled"]),
});

export type OrderFormData = z.infer<typeof orderSchema>;