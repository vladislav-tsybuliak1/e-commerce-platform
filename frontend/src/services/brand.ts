import {Brand} from '../types';
import {client} from '../utils/httpClient';

export async function getBrands(): Promise<Brand[]> {
  return client.get<Brand[]>('/brands/');
}
