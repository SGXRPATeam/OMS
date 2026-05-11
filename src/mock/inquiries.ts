import type { Inquiry } from "@/types/inquiry";

export const inquiries: Inquiry[] = [
  {
    id: "INQ-001",
    type: "inquiry",
    category: "Order Status",
    description: "Need update on shipment progress",
    status: "Open",
    createdAt: "2026-04-27",
  },
  {
    id: "CMP-001",
    type: "complaint",
    category: "Late Delivery",
    description: "Order delayed more than expected",
    status: "In Progress",
    createdAt: "2026-04-26",
  },
  {
    id: "DSP-001",
    type: "dispute",
    category: "Invoice",
    description: "Mismatch in invoice amount",
    status: "Resolved",
    createdAt: "2026-04-25",
  },
];