import {StockUnit} from './StockUnit';

export interface Product {
  id: number;
  name: string;
  description?: string;
  stock_unit: StockUnit;
  weight_product: boolean;
  stock_value: number;
  stock_quantity: number;
  price: number;
  image_url?: string;
  category_id: string;
  brand_id: string;
}
