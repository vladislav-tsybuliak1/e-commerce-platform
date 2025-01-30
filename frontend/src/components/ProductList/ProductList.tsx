import React from 'react';
import {ProductCard} from '../ProductCard';
import {Product} from '../../types';

type Props = {
  products: Product[];
  onDelete: (id: number) => void;
};

export const ProductList: React.FC<Props> = React.memo(
  ({products, onDelete}) => {
    console.log('product list')
    return (
      <div className="grid is-col-min-11">
        {products.map(product => (
          <div className="cell" key={product.id}>
            <ProductCard product={product} onDelete={onDelete}/>
          </div>
        ))}
      </div>
    );
  }
)