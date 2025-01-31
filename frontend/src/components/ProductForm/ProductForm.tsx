import React, {useEffect, useState} from 'react';
import {SubmitHandler, useForm, Controller} from 'react-hook-form';
import ReactSelect from 'react-select';
import {zodResolver} from '@hookform/resolvers/zod';
import {z} from 'zod';
import classNames from 'classnames';

import {Category, Brand, StockUnit, Product} from '../../types';
import {getBrands} from '../../services/brand';
import {getCategories} from '../../services/category';

import './ProductForm.scss';

const productSchema = z.object({
  name: z.string()
    .trim()
    .min(1, 'Provide the name')
    .max(255, 'Name must be at most 255 characters'),
  description: z
    .string()
    .trim()
    .max(1000, 'Description must be at most 1000 characters')
    .transform((value) => (
      (value === '' || value === undefined) ? null : value
    ))
    .nullable(),
  stock_unit: z.nativeEnum(StockUnit, {message: 'Make a selection'}),
  weight_product: z.boolean(),
  stock_value: z.coerce
    .number({message: 'Stock value must be a valid number'})
    .gt(0, 'Stock value must be greater than 0'),
  stock_quantity: z.coerce
    .number({message: 'Stock quantity must be a valid number'})
    .gte(0, 'Stock quantity must be at least 0'),
  price: z.coerce
    .number({message: 'Price must be a valid number'})
    .gte(0, 'Price must be at least 0')
    .transform((price) => price * 100),
  category_id: z.coerce
    .number({message: 'Make a selection'})
    .int()
    .positive('Make a selection'),
  brand_id: z.coerce
    .number({message: 'Make a selection'})
    .int()
    .positive('Make a selection'),
}).superRefine((data, ctx) => {
  // If weight_product is false, stock_quantity must be an integer
  if (!data.weight_product && !Number.isInteger(data.stock_quantity)) {
    ctx.addIssue({
      path: ['stock_quantity'],
      message: 'Stock quantity must be an integer if it is not a weight product',
      code: z.ZodIssueCode.custom,
    });
  }

  // Validation: If weight_product is true, stock_unit must be in ["KG", "G", "L", "ML"]
  if (data.weight_product && ['PCS', 'BOX'].includes(data.stock_unit)) {
    ctx.addIssue({
      path: ['stock_unit'],
      message: 'Weight product unit should be \'KG\', \'G\', \'L\', or \'ML\'',
      code: z.ZodIssueCode.custom,
    });
  }
});

type FormFields = z.infer<typeof productSchema>;

type Props = {
  onSubmit: (product: Product) => void;
  onReset?: () => void;
  product?: Product;
}

export const ProductForm: React.FC<Props> = React.memo(
  ({
     onSubmit,
     product,
     onReset = () => {
     }
   }) => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [brands, setBrands] = useState<Brand[]>([]);

    const units = Object.values(StockUnit);

    const {
      register,
      handleSubmit,
      setError,
      control,
      watch,
      reset,
      formState: {errors, isSubmitting, isSubmitSuccessful},
    } = useForm<FormFields>({
      defaultValues: product ? {...product, price: product.price / 100} : {},
      resolver: zodResolver(productSchema),
    });

    const handleProductSubmit: SubmitHandler<FormFields> = async (data) => {
      try {
        await new Promise((resolve) => setTimeout(resolve, 1000));

        const newProduct: Product = {
          ...data,
          id: product?.id || 0,
          image_url: product?.image_url || null,
        };

        onSubmit(newProduct);
        console.log(data);

      } catch (error) {
        setError('root', {message: String(error)})
      }
    };

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

    useEffect(() => {
      if (isSubmitSuccessful) {
        reset();
      }
    }, [reset, isSubmitSuccessful])


    console.log('product form');
    console.log(product);
    return (
      <form
        action=""
        className="box"
        onSubmit={handleSubmit(handleProductSubmit)}
        onReset={() => {
          reset();
          onReset();
        }}
      >

        <div className="field">
          <label className="label" htmlFor="product-name">Name</label>

          <div className="control">
            <input
              {...register('name')}
              className={classNames('input', {
                'is-danger': errors.name
              })}
              id="product-name"
              type="text"
              placeholder="Enter product name..."
            />
          </div>
          {errors.name && (
            <p className="help is-danger">{errors.name.message}</p>
          )}
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
            {...register('description')}
            className={classNames('textarea', {
              'is-danger': errors.description
            })}
            id="product-description"
            placeholder="Enter product description..."
          />
          </div>
          {errors.description && (
            <p className="help is-danger">{errors.description.message}</p>
          )}
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
              {...register('stock_value')}
              className={classNames('input', {
                'is-danger': errors.stock_value
              })}
              id="product-stock-value"
              type="text"
              placeholder="Enter value..."
            />
          </div>
          {errors.stock_value && (
            <p className="help is-danger">{errors.stock_value.message}</p>
          )}
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-stock-unit"
          >
            Stock unit
          </label>

          <div className="control has-icons-left">
            <div
              className={classNames('select', {
                'is-danger': errors.stock_unit
              })}
            >
              <select
                {...register('stock_unit')}
                id="product-stock-unit"
                defaultValue=""
              >
                <option
                  value=""
                  disabled={String(watch('stock_unit')) !== ''}
                >
                  Select unit
                </option>

                {units.map(value => (
                  <option value={value} key={value}>
                    {value.toLowerCase()}
                  </option>
                ))}
              </select>
            </div>
            <div className="icon is-small is-left">
              <i className="fas fa-scale-balanced"></i>
            </div>
          </div>

          {errors.stock_unit && (
            <p className="help is-danger">{errors.stock_unit.message}</p>
          )}
        </div>

        <div className="field">
          <div className="control">
            <label
              className="checkbox"
            >
              <input
                {...register('weight_product')}
                type="checkbox"
              />
              {` Weight product`}
            </label>
          </div>
          <p className="help">(only for kg, g, l, or ml)</p>

          {errors.weight_product && (
            <p className="help is-danger">{errors.weight_product.message}</p>
          )}
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
              {...register('stock_quantity')}
              className={classNames('input', {
                'is-danger': errors.stock_quantity
              })}
              id="product-stock-quantity"
              type="text"
              placeholder="Enter quantity value..."
            />
            <div className="icon is-small is-left">
              <i className="fas fa-warehouse"></i>
            </div>
          </div>

          <p className="help">(default value is 0)</p>

          {errors.stock_quantity && (
            <p className="help is-danger">{errors.stock_quantity.message}</p>
          )}
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
              {...register('price')}
              className={classNames('input', {
                'is-danger': errors.price
              })}
              id="product-price"
              type="text"
              placeholder="Enter price..."
            />
            <div className="icon is-small is-left">
              <i className="fas fa-coins"></i>
            </div>
          </div>

          <p className="help">(default value is 0)</p>

          {errors.price && (
            <p className="help is-danger">{errors.price.message}</p>
          )}
        </div>

        <div className="field">
          <label
            className="label"
            htmlFor="product-category-id"
          >
            Category
          </label>

          <div>
            <Controller
              name="category_id"
              control={control}
              render={({field}) => (
                <ReactSelect
                  {...field}
                  id="product-category-id"
                  options={categories.map((category) => ({
                    value: category.id,
                    label: category.name,
                  }))}
                  placeholder="Select category"
                  onChange={(selectedOption) => field.onChange(selectedOption?.value ?? null)}
                  value={
                    categories
                      .map((category) => ({
                        value: category.id,
                        label: category.name
                      }))
                      .find((option) => option.value === field.value) || null
                  }
                  isSearchable
                  isClearable
                  styles={{
                    control: (provided, state) => ({
                      ...provided,
                      border: errors.category_id
                        ? '1px solid hsl(348, 86%, 61%)'
                        : state.menuIsOpen
                          ? '1px solid hsl(217, 71%, 53%)'
                          : '1px solid #dbdbdb',
                      transition: 'box-shadow 0.2s ease-in-out',
                      boxShadow: errors.category_id && state.menuIsOpen
                        ? '0 0 0 3px hsl(348, 100%, 80%, 0.4)'
                        : state.menuIsOpen
                          ? '0 0 0 3px hsl(217, 71%, 53%, 0.25)'
                          : 'none',
                      cursor: 'pointer',
                      '&:hover': {
                        borderColor: errors.category_id
                          ? 'hsl(348, 86%, 55%)'
                          : state.menuIsOpen
                            ? 'hsl(217, 71%, 50%)'
                            : '#b5b5b5'
                      }
                    }),
                    placeholder: (provided) => ({
                      ...provided,
                      color: errors.category_id ? 'hsl(348deg, 100%, 21%)' : 'hsl(0, 0%, 14%)',
                    }),
                    dropdownIndicator: (provided) => ({
                      ...provided,
                      color: 'hsl(217, 71%, 53%)',
                    }),
                    indicatorSeparator: () => ({
                      display: 'none',
                    }),
                    option: (provided, state) => ({
                      ...provided,
                      backgroundColor: state.isFocused ? 'hsl(217, 71%, 53%)' : 'transparent',
                      color: errors.category_id && !state.isFocused
                        ? 'hsl(348deg, 100%, 21%)' :
                        state.isFocused
                          ? 'white'
                          : 'hsl(0, 0%, 14%)',
                      marginTop: '0',
                    }),
                    menu: (provided) => ({
                      ...provided,
                      marginTop: '0',
                      borderRadius: '0.375rem',
                    }),
                  }}
                />
              )}
            />
          </div>

          {errors.category_id && (
            <p className="help is-danger">{errors.category_id.message}</p>
          )}
        </div>

        <div className="field">
          <label className="label" htmlFor="product-brand-id">
            Brand
          </label>
          <div>
            <Controller
              name="brand_id"
              control={control}
              render={({field}) => (
                <ReactSelect
                  {...field}
                  id="product-brand-id"
                  options={brands.map((brand) => ({
                    value: brand.id,
                    label: brand.name,
                  }))}
                  placeholder="Select brand"
                  onChange={(selectedOption) => field.onChange(selectedOption?.value ?? null)}
                  value={
                    brands
                      .map((brand) => ({value: brand.id, label: brand.name}))
                      .find(option => option.value === field.value) || null
                  }
                  isSearchable
                  isClearable
                  styles={{
                    control: (provided, state) => ({
                      ...provided,
                      border: errors.brand_id
                        ? '1px solid hsl(348, 86%, 61%)'
                        : state.menuIsOpen
                          ? '1px solid hsl(217, 71%, 53%)'
                          : '1px solid #dbdbdb',
                      transition: 'box-shadow 0.2s ease-in-out',
                      boxShadow: errors.brand_id && state.menuIsOpen
                        ? '0 0 0 3px hsl(348, 100%, 80%, 0.4)'
                        : state.menuIsOpen
                          ? '0 0 0 3px hsl(217, 71%, 53%, 0.25)'
                          : 'none',
                      cursor: 'pointer',
                      '&:hover': {
                        borderColor: errors.brand_id
                          ? 'hsl(348, 86%, 55%)'
                          : state.menuIsOpen
                            ? 'hsl(217, 71%, 50%)'
                            : '#b5b5b5'
                      }
                    }),
                    placeholder: (provided) => ({
                      ...provided,
                      color: errors.brand_id ? 'hsl(348deg, 100%, 21%)' : 'hsl(0, 0%, 14%)',
                    }),
                    dropdownIndicator: (provided) => ({
                      ...provided,
                      color: 'hsl(217, 71%, 53%)',
                    }),
                    indicatorSeparator: () => ({
                      display: 'none',
                    }),
                    option: (provided, state) => ({
                      ...provided,
                      backgroundColor: state.isFocused ? 'hsl(217, 71%, 53%)' : 'transparent',
                      color: errors.brand_id && !state.isFocused
                        ? 'hsl(348deg, 100%, 21%)' :
                        state.isFocused
                          ? 'white'
                          : 'hsl(0, 0%, 14%)',
                      marginTop: '0',
                    }),
                    menu: (provided) => ({
                      ...provided,
                      marginTop: '0',
                      borderRadius: '0.375rem',
                    }),
                  }}
                />
              )}
            />
          </div>
          {errors.brand_id &&
            <p className="help is-danger">{errors.brand_id.message}</p>}
        </div>

        <div className="buttons">
          <button disabled={isSubmitting} type="submit"
                  className="button is-link">
            {isSubmitting ? 'Loading...' : 'Submit'}
          </button>

          <button type="reset" className="button is-link is-light">
            Cancel
          </button>
        </div>

        {errors.root && (
          <p className="help is-danger">{errors.root.message}</p>
        )}
      </form>
    );
  }
);