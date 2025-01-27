import React, {useEffect, useState} from 'react';
import {Product} from './types';
import {getProducts} from './services/product';
import {Loader} from './components/Loader';
import {ProductList} from './components/ProductList';

export const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [updatedAt, setUpdatedAt] = useState(new Date());

  useEffect(() => {
      setLoading(true);
      getProducts()
        .then(setProducts)
        .catch(() => setErrorMessage('Try again later'))
        .finally(() => setLoading(false))
    }, [updatedAt]
  )

  function reload() {
    setUpdatedAt(new Date());
    setErrorMessage('');
  }

  return (
    <div>
      <p className="title is-2">Products</p>
      <div>
        {loading && <Loader/>}

        {!loading && products.length > 0 && (
          <ProductList products={products}/>
        )}

        {!loading && !errorMessage && products.length === 0 && (
          <p className="title is-5">There are no products</p>
        )}

        {errorMessage && (
          <p className="notification is-danger">
            {errorMessage}
            <button onClick={reload}>Reload</button>
          </p>
        )}

      </div>
    </div>
  );
};
