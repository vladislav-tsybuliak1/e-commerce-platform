import {Product} from '../types';
import {getData} from '../utils/httpClient';

export function getProducts() {
  return getData<Product[]>('/products/')
    .then((products) => (products));
}
