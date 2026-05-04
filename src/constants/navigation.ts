import {
  LayoutDashboard,
  Package,
  Heart,
  ListOrdered,
  ClipboardList,
  MessageSquare,
  Phone,
  Settings,
} from "lucide-react";

export const NAV_ITEMS = [
  {
    name: "Dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Products",
    path: "/products",
    icon: Package,
  },
  {
    name: "Favourites",
    path: "/favourites",
    icon: Heart,
  },

  {
    name: "Order Type",
    icon: ClipboardList,
    children: [
      {
        name: "Orders",
        path: "/orders",
        icon: ListOrdered,
      },
      {
        name: "Non Orders",
        path: "/non-orders",
        icon: ClipboardList,
      },
    ],
  },

  {
    name: "Inquiries",
    path: "/inquiries",
    icon: MessageSquare,
  },
  {
    name: "Contact Us",
    path: "/contact",
    icon: Phone,
  },
  {
    name: "Settings",
    path: "/settings",
    icon: Settings,
  },
];