import React, {useEffect, useState} from 'react';
import {Category, Brand, StockUnit} from '../../types';
import {getBrands} from '../../services/brand';
import {getCategories} from '../../services/category.ts';

export const ProductForm: React.FC = React.memo(
  () => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [brands, setBrands] = useState<Brand[]>([]);

    const units = Object.values(StockUnit);

    useEffect(() => {
        getBrands()
          .then(setBrands)
          .catch()
          .finally();
        getCategories()
          .then(setCategories)
          .catch()
          .finally();
      }, []
    );

    return (
      <form
        action=""
        className="box"
      >
        <div className="field">
          <label className="label" htmlFor="product-name">Name</label>

          <div className="control">
            <input
              className="input"
              id="product-name"
              type="text"
              placeholder="Enter product name..."
            />
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-description"
          >
            Description
          </label>

          <div className="control">
          <textarea
            className="textarea"
            id="product-description"
            placeholder="Enter product description..."
          />
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-stock-value"
          >
            Stock value
          </label>

          <div className="control">
            <input
              className="input"
              id="product-stock-value"
              type="number"
              placeholder="Enter value..."
            />
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-stock-unit"
          >
            Stock unit
          </label>

          <div className="control has-icons-left">
            <div className="select is-rounded">
              <select
                id="product-stock-unit"
              >
                <option value="">Select unit</option>

                {units.map(value => (
                  <option value={value} key={value}>
                    {value}
                  </option>
                ))}
              </select>
            </div>
            <div className="icon is-small is-left">
              <i className="fas fa-scale-balanced"></i>
            </div>
          </div>
        </div>

        <div className="field">
          <div className="control">
            <label
              className="checkbox"
            >
              <input
                type="checkbox"
              />
              {` Weight product`}
            </label>
          </div>
          <p className="help">(only for kg, g, l, or ml)</p>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-stock-quantity"
          >
            Stock quantity
          </label>

          <div className="control has-icons-left">
            <input
              className="input"
              id="product-stock-quantity"
              type="number"
              placeholder="Enter quantity value..."
            />
            <div className="icon is-small is-left">
              <i className="fas fa-warehouse"></i>
            </div>
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-price"
          >
            Price, ₴
          </label>

          <div className="control has-icons-left">
            <input
              className="input"
              id="product-price"
              type="number"
              placeholder="Enter price..."
            />
            <div className="icon is-small is-left">
              <i className="fas fa-coins"></i>
            </div>
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-category-id"
          >
            Category
          </label>

          <div className="control has-icons-left">
            <div className="select is-rounded">
              <select
                id="product-category-id"
              >
                <option value="">Select category</option>

                {categories.map(category => (
                  <option
                    value={category.id}
                    key={category.id}
                  >
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="icon is-small is-left">
              <i className="fas fa-table"></i>
            </div>
          </div>
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-brand-id"
          >
            Brand
          </label>

          <div className="control has-icons-left">
            <div className="select is-rounded">
              <select
                id="product-brand-id"
              >
                <option value="">Select brand</option>

                {brands.map(brand => (
                  <option
                    value={brand.id}
                    key={brand.id}
                  >
                    {brand.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="icon is-small is-left">
              <i className="fas fa-trademark"></i>
            </div>
          </div>
        </div>

        <div className="buttons">
          <button type="submit" className="button is-link">
            Submit
          </button>

          <button type="reset" className="button is-link is-light">
            Cancel
          </button>
        </div>

      </form>
    );
  }
);