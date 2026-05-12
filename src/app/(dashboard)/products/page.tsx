
'use client';

import { useRouter } from 'next/navigation';
import ProductCardList from '@/modules/products/components/ProductCardList';

export default function MedicalProductsPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="max-w-7xl mx-auto mb-10">
        <h1 className="text-5xl font-bold text-slate-900">
          Medical Devices
        </h1>
      </div>

      <div className="max-w-7xl mx-auto">
        <ProductCardList
          onSelect={(product) =>
            router.push(
              `/orders?product=${encodeURIComponent(product.product_name)}&price=${product.unit_price}`
            )
          }
        />
      </div>
    </div>
  );
}