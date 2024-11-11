import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import './Products.css';
import { Select, MenuItem, FormControl, InputLabel, Slider, Typography, Button } from '@mui/material';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useUser } from '../../../context/UserContext';
import { useNavigate } from 'react-router-dom';
import Header from "../../Header";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const CategoryPage = () => {
  const query = useQuery();
  const category = query.get("query");
  const [products, setProducts] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);

  const [sortOption, setSortOption] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [maxPrice, setMaxPrice] = useState(500);

  const token = localStorage.getItem('authToken');
  const { currentUser } = useUser();
  const navigate = useNavigate();

  const filteredProducts = products
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

  const clearFilters = () => {
    setSelectedCondition('');
    setSelectedLocation('');
    setMaxPrice(500);
  }

  useEffect(() => {
    setLoading(true);
    fetch(`http://54.165.176.36:8000/api/products/?category=${category}`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((error) => console.error("Error fetching products:", error));
    axios.get('http://54.165.176.36:8000/api/product-choices/', {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => {
        const { categories, conditions, locations } = response.data;
        setConditions(conditions);
        setLocations(locations);
      })
      .catch(error => console.error('Error fetching preset values:', error));
  }, [category]);

  const handleOpenProduct = (id) => {
    navigate(`/products/${id}`);
  };

  return (
    <div style={{ height: '100vh' }}>
      <Header />

      <div className="products-container">
        <div className="filters">

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
              sx={{
                color: "#001f3f"
              }}
            />
          </FormControl>

          <Button
            onClick={() => { clearFilters() }}
            variant="outlined"
            sx={{
              '&:hover': {
              backgroundColor: '#007fa3',       // Custom hover color
              },
            }}
          >
            Clear Filters
          </Button>

        </div>
        <div className="product-grid">

          {loading ? (
            <span className="loader"></span>
          ) : (
            <>

              <div className="title">
                {category === 'textbook' ? (<h2>Textbooks</h2>) : (
                <h2>{category.charAt(0).toUpperCase() + category.slice(1)}</h2>)}
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
                    <div onClick={() => handleOpenProduct(product.id)}>

                      {product.image_url ?
                        (<img className="product-image" src={product.image_url}></img>)
                        : <img className="product-image" src="/images/no-image-icon.png"></img>}

                      <div className="product-text">
                        <div className="product-price">${product.price}</div>
                        <div className="product-title">{product.name}</div>
                        <div className="product-location">{product.pickup_location}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoryPage;
