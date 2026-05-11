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
import path from "path";

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
    path: "/favourite",
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

  // children: [
  //   {
  //     name: "Inquiry",
  //     path: "/inquiries",
  //     icon: MessageSquare,
  //   },
  //   {
  //     name: "Complaint List",
  //     path: "/inquiries/complaints",
  //     icon: MessageSquare,
  //   },
    
  //   {
  //     name: "Dispute List",
  //     path: "/inquiries/disputes",
  //     icon: MessageSquare,
  //   },
  // ],
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