import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

const Products = () => {
  const [products, setProducts] = useState([]);
  const token = localStorage.getItem('authToken');

  useEffect(() => {
    // Fetch products from the API
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
    <div>
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
    </div>
  );
};

export default Products;
