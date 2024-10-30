import React, { useState, useEffect } from "react";
import './Products.css';
import { Select, MenuItem, FormControl, InputLabel, Slider, Typography, Button } from '@mui/material';
import axios from 'axios';
import {Link} from 'react-router-dom'; 
import { useUser } from '../../context/UserContext';
import { useNavigate } from 'react-router-dom';

import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [locations, setLocations] = useState([]);

  const [sortOption, setSortOption] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [maxPrice, setMaxPrice] = useState(500);

  const token = localStorage.getItem('authToken');
  const { currentUser } = useUser();
  const navigate = useNavigate();

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

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedCondition('');
    setSelectedLocation('');
    setMaxPrice(500);
  }

  const hour = parseInt(new Date().getHours());
  let greeting = '';
  if (5 <= hour && hour <= 11) {
    greeting = 'Good morning';
  } else if (12 <= hour && hour <= 17) {
    greeting = 'Good afternoon';
  } else if (18 <= hour && hour <= 20) {
    greeting = 'Good evening';
  } else if ((21 <= hour && hour <= 23) || hour <= 4) {
    greeting = 'Welcome back';
  }

  const responsive = {
    allScreens: {
      breakpoint: { max: 4000, min: 0 },
      items: 1,
    },
  };


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

  const handleOpenProduct = (id) => {
    navigate(`/products/${id}`);
  };

  return (
    <div>
      <div className="product-grid">
          {currentUser ? (<h1 style={{textAlign: "left", padding: "0 45px", margin: "35px 0 0 0"}}>{greeting}, {currentUser.first_name}</h1>) : null} 
          
          <Carousel
            responsive={responsive}
            swipeable={true}
            draggable={true}
            showDots={true}
            infinite={true}
            autoPlay={true}
            autoPlaySpeed={2000}
            keyBoardControl={true}
            customTransition="all 0.5s"
            transitionDuration={500}
            containerClass="carousel-container"
            removeArrowOnDeviceType={["tablet", "mobile"]}
            dotListClass="custom-dot-list-style"
            itemClass="carousel-item-padding-40-px"
          >
            <div>Item 1</div>
            <div>Item 2</div>
            <div>Item 3</div>
            <div>Item 4</div>
            <div>Item 5</div>
          </Carousel>
        
          <div className="title">
            <h2>Featured listings</h2>
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
        </div>
    </div>
  );
};

export default Products;
