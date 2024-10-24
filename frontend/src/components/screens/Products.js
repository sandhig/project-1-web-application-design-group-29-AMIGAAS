import React, { useState, useEffect } from "react";
import './Products.css';

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
        <div className="filters">
          filters
        </div>
        <div className="products">
        <div className="product-grid">
          {products.map(product => (
            <div key={product.id} className="product-item">
              <h3>{product.name}</h3>
              <p>${product.price}</p>
            </div>
          ))}
        </div>
        </div>
    </div>
  );
};

export default Products;
