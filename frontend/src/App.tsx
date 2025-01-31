import React, {useCallback, useEffect, useState} from 'react';
import {Product} from './types';
import {getProducts} from './services/product';
import {Loader} from './components/Loader';
import {ProductList} from './components/ProductList';
import {ProductForm} from './components/ProductForm';

export const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [updatedAt, setUpdatedAt] = useState(new Date());
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)

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
        <p className="title is-2">Products</p>
        <div>
          {loading && <Loader/>}

          {!loading && products.length > 0 && (
            <ProductList
              products={products}
              onDelete={deleteProduct}
              onSelect={setSelectedProduct}
              selectedProductId={selectedProduct?.id}
            />
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
    </div>
  );
};
