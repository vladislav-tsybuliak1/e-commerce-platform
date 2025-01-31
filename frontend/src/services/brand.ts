import {Brand} from '../types';
import {client} from '../utils/httpClient';

export async function getBrands() {
  return client.get<Brand[]>('/brands/')
    .then((brands) => (brands));
}
