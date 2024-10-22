import React, { useState, useEffect } from "react";
import axios from "axios";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    description: "",
  });
  /*
  useEffect(() => {
    
    const token = localStorage.getItem('authToken');
    
    fetch("http://3.87.240.14:8000/api/products/", {
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      return response.json();
    })
    .then(data => {
      setProducts(data);
    })
    .catch(error => {
      console.error("There was an error fetching the products!", error);
    });
  }, []);
  */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct({
      ...newProduct,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('authToken');
    axios
      .post("http://3.87.240.14:8000/api/products/", newProduct, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      })
      .then((response) => {
        setProducts([...products, response.data]);
        setNewProduct({ name: "", description: "" });
      })
      .catch((error) => {
        console.error("There was an error creating the product!", error);
      });
      
  };
  
  

  return (
    <div>
      <h2>Products</h2>
      <h3>Coming soon...</h3>
      
      {/*
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name}
            <p>{product.description}</p>
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Product Name"
          value={newProduct.name}
          onChange={handleInputChange}
        />
        <textarea
          name="description"
          placeholder="Product Description"
          value={newProduct.description}
          onChange={handleInputChange}
        />
        <button type="submit">Add Product</button>
      </form>
      */}
    </div>
  );
};

export default Products;
