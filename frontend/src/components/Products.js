import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

const Products = () => {
  const [products, setProducts] = useState([]);

  // Fetch products from the backend
  useEffect(() => {
    axios
      .get("http://localhost:8000/api/products/")
      .then((response) => {
        setProducts(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the products!", error);
      });
  }, []);
  
  return (
    <div>
        <h2>Products</h2>
        <Link to="/products/create">
            <button className="button">Create Listing</button>
        </Link>
        {/* List Products */}
        <ul>
            {products.map((product) => (
                <li key={product.id}>
                    {product.name}
                    <p>{product.description}</p>
                </li>
            ))}
        </ul>
    </div>
  );
};

export default Products;