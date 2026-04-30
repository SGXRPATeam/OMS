import DashboardLayout from "@/components/layout/DashboardLayout";
import { SearchProvider } from "@/context/SearchContext";

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SearchProvider>
      <DashboardLayout>{children}</DashboardLayout>
    </SearchProvider>
  );
}