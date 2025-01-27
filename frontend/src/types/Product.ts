import {StockUnit} from './StockUnit.ts';

export interface Product {
  id: number;
  name: string;
  description: string | null;
  stock_unit: StockUnit;
  weight_product: boolean;
  stock_value: number;
  stock_quantity: number;
  price: number;
  image_url: string | null;
  category: string;
  brand: string;
}
