import React, { useState, useEffect } from "react";
import axios from "axios";
import './CreateListing.css'
import './UploadAndDisplayImage.js'
import UploadAndDisplayImage from "./UploadAndDisplayImage.js";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    title: "",
    price: "",
    description: "",
    category: "",
    condition: "",
    pickupLocation: "",
  });
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [selectedPickupLocation, setSelectedPickupLocation] = useState('');

  const categories = [
    { id: 1, name: 'Category 1' },
    { id: 2, name: 'Category 2' },
    { id: 3, name: 'Category 3' },
    { id: 4, name: 'Category 4' },
  ];

  const condition = [
    { id: 1, name: 'New' },
    { id: 2, name: 'Used - Like New' },
    { id: 3, name: 'Used - Good' },
    { id: 4, name: 'Used - Fair' },
  ];

  const pickupLocation = [
    { id: 1, name: 'Robarts' },
    { id: 2, name: 'Gerstein' },
    { id: 3, name: 'Computer Science Library' },
    { id: 4, name: 'Bahen' },
    { id: 5, name: 'Galbraith' },
    { id: 6, name: 'Sanford Fleming' },
    { id: 7, name: 'Bahen' },
  ];

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct({
      ...newProduct,
      [name]: value,
    });
  };

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
    setNewProduct({
      ...newProduct,
      category: e.target.value,
    });
  };

  const handleConditionChange = (e) => {
    setSelectedCondition(e.target.value);
    setNewProduct({
      ...newProduct,
      condition: e.target.value,
    });
  };

  const handlePickupLocationChange = (e) => {
    setSelectedPickupLocation(e.target.value);
    setNewProduct({
      ...newProduct,
      pickupLocation: e.target.value,
    });
  };

  // Submit new product to the backend
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("userId", 1); // Example user ID, replace with dynamic value
    formData.append("name", newProduct.title); 
    formData.append("price", newProduct.price); 
    formData.append("category", newProduct.category); 
    formData.append("condition", newProduct.condition); 
    formData.append("pickup_location", newProduct.pickupLocation); 
    formData.append("photo", newProduct.photo); // Add photo to form data
    if (newProduct.description) formData.append("description", newProduct.description); 
    if (newProduct.size) formData.append("size", newProduct.size); // optional
    if (newProduct.colour) formData.append("colour", newProduct.colour);

    axios.post("http://localhost:8000/api/products/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
      .then((response) => {
        setProducts([...products, response.data]); // Add the new product to the list
        setNewProduct({ title: "", price: "", category: "", condition: "", pickupLocation: "", description: "" }); // Reset form
        setSelectedCategory("");
        setSelectedCondition("");
        setSelectedPickupLocation("");
      })
      .catch((error) => {
        console.error("There was an error creating the listing!", error);
      });
  };
  
  return (
    <div>
      <h2 className="column-container">Products</h2>
      {/* Form to Add New Listing */}
      <form onSubmit={handleSubmit}>
        <div className="column-container">
          <input 
            className="column-item"
            type="text"
            name="title"
            placeholder="Title"
            value={newProduct.title}
            onChange={handleInputChange}
          />
          <UploadAndDisplayImage /> 
          <input
            className="column-item"
            type="number"
            name="price"
            placeholder="Price"
            value={newProduct.price}
            onChange={handleInputChange}
          />
          <label className="column-item">
            Category:
            <select value={selectedCategory} onChange={handleCategoryChange}>
              <option value="" disabled>Select an option</option>
              {categories.map(category => (
                <option value={`${category.id}`}>{category.name}</option>
              ))}
            </select>
          </label>
          <label className="column-item space-right">
            Condition:
            <select value={selectedCondition} onChange={handleConditionChange}>
              <option value="" disabled>Select an option</option>
              {condition.map(condition => (
                <option value={`${condition.id}`}>{condition.name}</option>
              ))}
            </select>
          </label>
          <label className="column-item">
            Pickup Location:
            <select value={selectedPickupLocation} onChange={handlePickupLocationChange}>
              <option value="" disabled>Select an option</option>
              {pickupLocation.map(location => (
                <option value={`${location.id}`}>{location.name}</option>
              ))}
            </select>
          </label>
          <textarea
            className="column-item"
            name="description"
            placeholder="Product Description"
            value={newProduct.description}
            onChange={handleInputChange}
          />
          <button className="column-item" type="submit">Add Listing</button>
        </div>
      </form>
    </div>
  );
};

export default Products;