import React, {useCallback, useEffect, useMemo, useState} from 'react';
import debounce from 'lodash.debounce';

import {Product} from './types';
import {getProducts} from './services/product';
import {Loader} from './components/Loader';
import {ProductList} from './components/ProductList';
import {ProductForm} from './components/ProductForm';

// function debounce(callback: Function, delay: number) {
//   let timerId = 0;
//   return (...args: any) => {
//     window.clearTimeout(timerId);
//
//     timerId = window.setTimeout(() => {
//       callback(...args);
//     }, delay);
//   };
// }

export const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [updatedAt, setUpdatedAt] = useState(new Date());
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)

  const [query, setQuery] = useState('');
  const [appliedQuery, setAppliedQuery] = useState('')

  const debouncedSetQuery = useMemo(
    () => debounce(setAppliedQuery, 1000),
    [setAppliedQuery],
  );

  const applyQuery = useCallback((query: string) => {
    debouncedSetQuery(query);
  }, [debouncedSetQuery]);

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
    applyQuery(event.target.value);
  };

  const filteredProducts = useMemo(() => (
    products.filter(product => product.name.toLowerCase().includes(appliedQuery.toLowerCase()))
  ), [appliedQuery, products])

  const [counter, setCounter] = useState(0)

  useEffect(() => {
      setLoading(true);
      getProducts()
        .then(setProducts)
        .catch(() => setErrorMessage('Try again later'))
        .finally(() => setLoading(false))
    }, [updatedAt]
  )

  const addProduct = useCallback((newProduct: Product) => {
      setProducts(currentProducts => [newProduct, ...currentProducts])
    }, []
  );

  const deleteProduct = useCallback((productId: number) => {
      setProducts(currentProducts => currentProducts.filter(product => product.id !== productId));
    }, []
  );

  const updateProduct = useCallback((updatedProduct: Product) => {
      setProducts(currentProducts => {
        const newProducts = [...currentProducts];
        const index = newProducts.findIndex(product => product.id === updatedProduct.id);

        newProducts.splice(index, 1, updatedProduct);

        return newProducts;
      });

      setSelectedProduct(null);
    }, []
  );

  function reload() {
    setUpdatedAt(new Date());
    setErrorMessage('');
  }

  console.log(products);

  return (
    <div>
      <div>
        <p className="title is-2">Add a new product</p>
        {selectedProduct ? (
          <ProductForm
            onSubmit={updateProduct}
            product={selectedProduct}
            key={selectedProduct.id}
            onReset={() => setSelectedProduct(null)}
          />
        ) : (
          <ProductForm onSubmit={addProduct}/>
        )}
      </div>

      <button onClick={() => setCounter(x => x + 1)}>
        {counter}
      </button>


      <div>
        <div className="columns">
          <div className="column">
            <p className="title is-2">Products</p>
          </div>
          <div className="column">
            <input
              type="text"
              className="input is-rounded"
              value={query}
              onChange={handleQueryChange}
            />
          </div>
        </div>
        <div>
          {loading && <Loader/>}

          {!loading && filteredProducts.length > 0 && (
            <ProductList
              products={filteredProducts}
              onDelete={deleteProduct}
              onSelect={setSelectedProduct}
              selectedProductId={selectedProduct?.id}
            />
          )}

          {!loading && !errorMessage && filteredProducts.length === 0 && (
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
    </div>
  );
};
