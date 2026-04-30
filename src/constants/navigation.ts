import {
  LayoutDashboard,
  Package,
  Heart,
  ListOrdered,
  MessageSquare,
  Phone,
  Settings,
} from "lucide-react";

export const NAV_ITEMS = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Products", path: "/products", icon: Package },
  { name: "Favourites", path: "/favourites", icon: Heart },
  { name: "Order Lists", path: "/orders", icon: ListOrdered },
  { name: "Inquiries", path: "/inquiries", icon: MessageSquare },
  { name: "Contact Us", path: "/contact", icon: Phone },
  { name: "Settings", path: "/settings", icon: Settings },
];