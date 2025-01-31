import {Product} from '../types';
import {client} from '../utils/httpClient';

export async function getProducts(): Promise<Product[]> {
  return await client.get<Product[]>('/products/')
}

export async function deleteProduct(productId: number): Promise<void> {
  return client.delete<void>(`/products/${productId}/`)
}

export async function createProduct(
  product: Omit<Product, 'id' | 'image'>
): Promise<Product> {
  return await client.post<Product>('/products/', product);
}

export async function updateProduct(
  product: Omit<Product, 'image'>
): Promise<Product> {
  const {id, ...data} = product;
  return await client.put<Product>(`/products/${id}/`, data);
}
