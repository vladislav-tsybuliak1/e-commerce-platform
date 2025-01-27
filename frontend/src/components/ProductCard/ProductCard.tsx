import React from 'react';
import {Product} from '../../types'

type Props = {
  product: Product;
}

export const ProductCard: React.FC<Props> = ({product}) => {
  return (
    <div className="card">
      <div className="card-image">
        <figure className="image is-aspect-ratio-1by1">
          <img
            src={product.image_url ? product.image_url : "https://placehold.co/600x600"}
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

      </div>
    </div>
  );
};