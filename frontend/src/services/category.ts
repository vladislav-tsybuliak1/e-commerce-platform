import {Category} from '../types';
import {client} from '../utils/httpClient';

export async function getCategories(): Promise<Category[]> {
  return await client.get<Category[]>('/categories/');
}
