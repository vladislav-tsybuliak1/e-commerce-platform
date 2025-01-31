import {Product} from '../types';
import {client} from '../utils/httpClient';

export async function getProducts() {
  return client.get<Product[]>('/products/')
    .then((products) => (products));
}

export async function deleteProduct(productId: number) {
  return client.delete<Product[]>(`/products/${productId}/`)
}