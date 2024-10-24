import React, { useState, useEffect } from "react";
import './Products.css';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [sortOption, setSortOption] = useState('');
  const token = localStorage.getItem('authToken');

  const sortedProducts = [...products].sort((a, b) => {
    if (sortOption === 'priceAsc') {
      return a.price - b.price;
    } else if (sortOption === 'priceDesc') {
      return b.price - a.price;
    } else if (sortOption === 'nameAsc') {
      return a.name.localeCompare(b.name);
    }
    return 0;
  });

  useEffect(() => {
    fetch('http://3.87.240.14:8000/api/products/', {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Error fetching products:', error));
  }, []);

  return (
    <div className="products-container">
        <div className="filters">
          filters
        </div>
        <div className="product-grid">

          <div className="title">
            <h1>Featured listings</h1>
            <FormControl className="sort-by" variant="outlined" style={{ minWidth: 200, marginBottom: '20px' }}>
              <InputLabel id="sort-label">Sort By</InputLabel>
              <Select
                labelId="sort-label"
                value={sortOption}
                onChange={(e) => setSortOption(e.target.value)}
                label="Sort By"
              >
                <MenuItem value="priceAsc">Price: Low to High</MenuItem>
                <MenuItem value="priceDesc">Price: High to Low</MenuItem>
                <MenuItem value="nameAsc">Name: A-Z</MenuItem>
              </Select>
            </FormControl>
          </div>

          <div className="products">
            {sortedProducts.map(product => (
              <div key={product.id} className="product-item">
                <img className="product-image" src={product.image_url}></img>
                <div className="product-text">
                  <div className="product-price">${product.price}</div>
                  <div className="product-title">{product.name}</div>
                  <div className="product-location">{product.pickup_location}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
    </div>
  );
};

export default Products;
