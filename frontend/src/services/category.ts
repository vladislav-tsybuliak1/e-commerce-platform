import {Category} from '../types';
import {client} from '../utils/httpClient';

export async function getCategories() {
  return client.get<Category[]>('/categories/')
    .then((categories) => (categories));
}
