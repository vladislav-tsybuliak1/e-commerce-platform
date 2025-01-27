import React from 'react';
import productsFromServer from './products.json';
import {ProductCard} from "./components/ProductCard";

export const App: React.FC = () => {
  return (
    <div>
      <p>Products</p>
      <div className="grid is-col-min-11">
        {productsFromServer.map(product => (
          <div className="cell">
            <ProductCard key={product.id} product={product}/>
          </div>
        ))}
      </div>
    </div>
  );
};
