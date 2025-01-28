import {Category} from '../types';
import {getData} from '../utils/httpClient';

export function getCategories() {
  return getData<Category[]>('/categories/')
    .then((categories) => (categories));
}
