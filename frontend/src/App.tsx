import React, {useEffect, useState} from 'react';
import {Product} from './types';
import {getProducts} from './services/product.tsx';
import {Loader} from './components/Loader';
import {ProductList} from './components/ProductList';

export const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
      setLoading(true);
      getProducts()
        .then(setProducts)
        .catch(() => setErrorMessage('Try again later'))
        .finally(() => setLoading(false))
    }, []
  )
  return (
    <div>
      <p className="title is-2">Products</p>
      <div>
        {loading && <Loader/>}

        {!loading && products.length > 0 && (
          <ProductList products={products}/>
        )}

        {!loading && products.length === 0 && (
          <p className="title is-5">There are no products</p>
        )}

        {errorMessage && (
          <p className="notification is-danger">{errorMessage}</p>
        )}

      </div>
    </div>
  );
};
