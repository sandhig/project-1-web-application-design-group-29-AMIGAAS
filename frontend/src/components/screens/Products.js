import React, { useState, useEffect } from "react";
import './Products.css';
import { Select, MenuItem, FormControl, InputLabel, Slider, Typography } from '@mui/material';
import axios from 'axios';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [locations, setLocations] = useState([]);

  const [sortOption, setSortOption] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [maxPrice, setMaxPrice] = useState(100);

  const token = localStorage.getItem('authToken');

  const filteredProducts = products

  .filter(product => {
    if (selectedCategory) {
      return product.category === selectedCategory.value;
    }
    return true;
  })

  .filter(product => {
    if (selectedCondition) {
      return product.condition === selectedCondition.value;
    }
    return true;
  })

  .filter(product => {
    if (selectedLocation) {
      return product.pickup_location === selectedLocation.value;
    }
    return true;
  })

  .filter(product => {
    if (maxPrice === 500) {
      return true;
    }
    return product.price <= maxPrice;
  })

  .sort((a, b) => {
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
      axios.get('http://3.87.240.14:8000/api/product-choices/', {
        headers: {
          'Authorization': `Token ${token}`,
        }
    })
      .then(response => {
        const { categories, conditions, locations } = response.data;
        setCategories(categories);
        setConditions(conditions);
        setLocations(locations);
      })
      .catch(error => console.error('Error fetching preset values:', error));
  }, []);

  return (
    <div className="products-container">
        <div className="filters">

          <FormControl className="category-filter" variant="outlined">
            <InputLabel id="category-label">Category</InputLabel>
            <Select
              labelId="category-label"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              label="Category"
            >
              <MenuItem value=""><em>None</em></MenuItem>
              {categories.map((category, index) => (
                <MenuItem key={index} value={category}>
                  {category.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl className="condition-filter" variant="outlined">
            <InputLabel id="condition-label">Condition</InputLabel>
            <Select
              labelId="condition-label"
              value={selectedCondition}
              onChange={(e) => setSelectedCondition(e.target.value)}
              label="Condition"
            >
              <MenuItem value=""><em>None</em></MenuItem>
              {conditions.map((condition, index) => (
                <MenuItem key={index} value={condition}>
                  {condition.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl className="location-filter" variant="outlined">
            <InputLabel id="location-label">Location</InputLabel>
            <Select
              labelId="location-label"
              value={selectedLocation}
              onChange={(e) => setSelectedLocation(e.target.value)}
              label="Location"
            >
              <MenuItem value=""><em>None</em></MenuItem>
              {locations.map((location, index) => (
                <MenuItem key={index} value={location}>
                  {location.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl className="price-filter" variant="outlined">
            <Typography id="max-price-slider" gutterBottom>
              Max Price
            </Typography>
            <Slider
              value={maxPrice}
              onChange={(e, newValue) => setMaxPrice(newValue)}
              valueLabelDisplay="auto"
              aria-labelledby="max-price-slider"
              min={0}
              max={500}
              step={10}
              marks={[
                { value: 500, label: '500+' }
              ]}
            />
          </FormControl>

        </div>
        <div className="product-grid">

          <div className="title">
            <h1>Featured listings</h1>
            <FormControl className="sort-by" variant="outlined">
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
            {filteredProducts.map(product => (
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
