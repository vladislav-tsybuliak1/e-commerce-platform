import {StockUnit} from './StockUnit';
import {Category} from './Category';
import {Brand} from './Brand';

export interface Product {
  id: number;
  name: string;
  description: string | null;
  stock_unit: StockUnit;
  weight_product: boolean;
  stock_value: number;
  stock_quantity: number;
  price: number;
  image: string | null;
  category_id: number;
  brand_id: number;
  category?: Category;
  brand?: Brand;
}
