import { apiFetch } from "@/lib/api";

export const OrderService = {
  getAll: () => apiFetch("/orders"),

  create: (payload: any) =>
    apiFetch("/orders", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  update: (
    id: string,
    payload: any
  ) =>
    apiFetch(`/orders/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),

  delete: (id: string) =>
    apiFetch(`/orders/${id}`, {
      method: "DELETE",
    }),
};