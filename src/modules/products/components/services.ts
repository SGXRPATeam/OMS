import { Product } from '@/types/product';

const API_URL =
  'http://127.0.0.1:8000';

export async function getProducts(): Promise<Product[]> {
  const token =
    localStorage.getItem('token');

  const response = await fetch(
    `${API_URL}/products`,
    {
      method: 'GET',
      headers: {
        'Content-Type':
          'application/json',
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(
      'Failed to fetch products'
    );
  }

  return response.json();
}