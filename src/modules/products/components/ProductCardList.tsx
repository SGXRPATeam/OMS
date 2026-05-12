'use client';

import { useEffect, useState } from 'react';

import { getProducts } from './services';

import { Product } from '@/types/product';

type Props = {
  onSelect?: (product: Product) => void;
};

export default function ProductCardList({
  onSelect,
}: Props) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);

      const data =
        await getProducts();

      setProducts(data);
    } catch (err: any) {
      setError(
        err.message ||
          'Failed to load products'
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-20 text-slate-500">
        Loading products...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-20 text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div className="grid gap-8 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {products.map((product) => (
        <div
          key={product.product_id}
          className="bg-white rounded-3xl border border-slate-200 shadow-sm hover:shadow-xl transition duration-300 overflow-hidden group"
        >
          {/* Image */}
          <div className="h-64 bg-white p-6">
            <img
              src={
                product.image_url ||
                '/placeholder.png'
              }
              alt={product.product_name}
              className="w-full h-full object-contain group-hover:scale-105 transition duration-500"
            />
          </div>

          {/* Content */}
          <div className="p-5">
            <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
              {
                product.product_category
              }
            </span>

            <h2 className="mt-3 text-xl font-bold text-slate-900">
              {product.product_name}
            </h2>

            <p className="mt-2 text-sm text-slate-500 leading-6">
              {product.description}
            </p>

            {/* Price */}
            <div className="mt-4 flex items-center gap-3 flex-wrap">
              <span className="text-2xl font-bold text-blue-600">
                ₹
                {product.unit_price.toLocaleString()}
              </span>
            </div>

            {/* Stock */}
            <div className="mt-2 text-sm text-slate-500">
              Stock:
              {' '}
              {product.stock_qty}
              {' '}
              {product.uom}
            </div>

            {/* Button */}
            <button
              onClick={() =>
                onSelect?.(product)
              }
              className="mt-5 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold transition"
            >
              Order Device
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}