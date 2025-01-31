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

export async function updateProduct(
  product: Omit<Product, 'image'>
) {
  const { id, ...data } = product;
  return client.put<Product, Omit<typeof product, 'id'>>(`/products/${id}/`, data);
}
