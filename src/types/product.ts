export interface Product {
  product_id: string;
  tenantid: string;
  product_code: string;
  product_name: string;
  product_type: string;
  product_category: string;
  product_sub_category?: string;
  description?: string;
  unit_price: number;
  currency: string;
  sku_code?: string;
  stock_qty: number;
  uom: string;
  image_url?: string;
  product_status: string;
}