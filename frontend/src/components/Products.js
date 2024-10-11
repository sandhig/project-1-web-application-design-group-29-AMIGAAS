import React, { useState, useEffect } from "react";
import axios from "axios";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    description: "",
  });

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

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct({
      ...newProduct,
      [name]: value,
    });
  };

  // Submit new product to the backend
  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://localhost:8000/api/products/", newProduct)
      .then((response) => {
        setProducts([...products, response.data]); // Add the new product to the list
        setNewProduct({ name: "", description: "" }); // Reset form
      })
      .catch((error) => {
        console.error("There was an error creating the product!", error);
      });
  };

  return (
    <div>
      <h2>Products</h2>

      {/* List Products */}
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name}
            <p>{product.description}</p>
          </li>
        ))}
      </ul>

      {/* Form to Add New Product */}
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
    </div>
  );
};

export default Products;
