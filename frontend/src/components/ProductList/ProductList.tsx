import React from 'react';
import {ProductCard} from '../ProductCard';
import {Product} from '../../types';

type Props = {
  products: Product[];
};

export const ProductList: React.FC<Props> = React.memo(
  ({products}) => {
    return (
      <div className="grid is-col-min-11">
        {products.map(product => (
          <div className="cell" key={product.id}>
            <ProductCard product={product}/>
          </div>
        ))}
      </div>
    );
  }
)