import React from 'react';
import {Product} from '../../types'
import classNames from 'classnames';
import {HOST_URL} from '../../utils/httpClient';

type Props = {
  product: Product;
  selectedProductId?: number;
  onDelete: (id: number) => void;
  onSelect: (product: Product) => void;
}

export const ProductCard: React.FC<Props> = (
  {
    product,
    selectedProductId,
    onDelete = () => {
    },
    onSelect = () => {
    },
  }) => {
  return (
    <div className={classNames('card', {
      'has-background-info': product.id === selectedProductId,
    })}>
      <div className="card-image">
        <figure className="image is-aspect-ratio-1by1">
          <img
            src={product.image ? `${HOST_URL}/${product.image}` : 'https://placehold.co/600x600'}
            alt="Placeholder image"
          />
        </figure>
      </div>
      <div className="card-content">
        <p className="title is-4">
          {product.price / 100} ₴
        </p>
        <p className="subtitle is-5">
          {product.name.slice(0, 40)}{product.name.length > 40 && '...'}
        </p>
        <p className="title is-6">
          {product.stock_value}{product.stock_unit.toLowerCase()}
        </p>
        <div className="buttons">
          <button
            className="icon button has-background-white is-info is-inverted"
            onClick={() => onSelect(product)}
          >
            <i className="fas fa-pen"></i>
          </button>
          <button
            className="icon button has-background-white is-danger is-inverted"
            onClick={() => onDelete(product.id)}
          >
            <i className="fas fa-xmark"></i>
          </button>
        </div>
      </div>
    </div>
  );
};