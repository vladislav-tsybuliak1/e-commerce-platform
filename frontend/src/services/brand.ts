import {Brand} from '../types';
import {getData} from '../utils/httpClient';

export function getBrands() {
  return getData<Brand[]>('/brands/')
    .then((brands) => (brands));
}
