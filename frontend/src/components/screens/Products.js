import React, { useState, useEffect } from "react";
import './Products.css';
import { Link } from 'react-router-dom';

import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import MessageIcon from '@mui/icons-material/Message';
import TextField from "@mui/material/TextField";

const Products = () => {
  const [products, setProducts] = useState([]);
  const token = localStorage.getItem('authToken');

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
      {/*
      <h2>Products</h2>
      <Link to="/products/create">
            <button className="button">Create Listing</button>
      </Link>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            {product.name} - ${product.price}
          </li>
        ))}
      </ul>
        */}
        <div className="filters">
          filters
        </div>
        <div className="products">
          products
        </div>
    </div>
  );
};

export default Products;
