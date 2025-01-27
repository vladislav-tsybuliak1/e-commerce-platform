import {Product} from '../types';

export function getProducts(): Promise<Product[]> {
  return fetch('http://127.0.0.1:8000/api/v1/products/')
    .then((response) => {
      if (!response.ok) {
        return;
      }
      return response.json();
    })
    .then((products) => (products));
}
