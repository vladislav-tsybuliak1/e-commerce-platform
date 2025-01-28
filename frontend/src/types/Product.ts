import {StockUnit} from './StockUnit';

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
  category_id: string;
  brand_id: string;
}
