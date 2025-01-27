import React, {useEffect, useState} from 'react';
import {ProductCard} from './components/ProductCard';
import {Product} from './types';
import {getProducts} from './services/product.tsx';

export const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
      getProducts().then(setProducts)
    }, []
  )
  return (
    <div>
      <p>Products</p>
      <div className="grid is-col-min-11">
        {products.map(product => (
          <div className="cell" key={product.id}>
            <ProductCard product={product}/>
          </div>
        ))}
      </div>

    </div>
  );
};
