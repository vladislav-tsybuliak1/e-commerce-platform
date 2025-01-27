export interface Product {
  id: number;
  name: string;
  description: string | null;
  stock_unit: string;
  weight_product: boolean;
  stock_value: number;
  stock_quantity: number;
  price: number;
  image_url: string | null;
  category: string;
  brand: string;
}
