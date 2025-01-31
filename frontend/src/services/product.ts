import {Product} from '../types';
import {client} from '../utils/httpClient';

export async function getProducts() {
  return client.get<Product[]>('/products/')
    .then((products) => (products));
}

export async function deleteProduct(productId: number) {
  return client.delete<null>(`/products/${productId}/`)
}

export async function createProduct(
  product: Omit<Product, 'id' | 'image'>
) {
  return client.post<Product, typeof product>('/products/', product);
}
