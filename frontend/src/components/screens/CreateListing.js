import React, { useState, useEffect } from 'react';
import { TextField, MenuItem, Select, InputLabel, FormControl, Button, Box, InputAdornment } from '@mui/material';
import axios from 'axios';
import { useUser } from '../../context/UserContext';

function CreateListing() {
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
    condition: '',
    location: '',
    description: ''
  });

  const { currentUser } = useUser();
  const token = localStorage.getItem('authToken');

  const [categories, setCategories] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [locations, setLocations] = useState([]);

  useEffect(() => {
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

  const handleInputChange = (event) => {
    const { name, value } = event.target;

    if (name === 'price') {
      const validPrice = value.match(/^\d*(\.\d{0,2})?$/);
      if (validPrice) {
        setFormData({
          ...formData,
          [name]: value
        });
      }
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const payload = {
      name: formData.name,
      price: parseFloat(formData.price),
      category: formData.category.value,
      condition: formData.condition.value,
      pickup_location: formData.location.value,
      description: formData.description
    };

    axios.post('http://3.87.240.14:8000/api/products/', payload, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    })
      .then(response => {
        console.log('Product added:', response.data);
      })
      .catch(error => console.error('Error adding product:', error));
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        maxWidth: 300,
        margin: 'auto'
      }}
    >
      <TextField
        label="name"
        name="name"
        value={formData.name}
        onChange={handleInputChange}
        variant="outlined"
        required
      />

      <TextField
        label="Price"
        name="price"
        type="number"
        value={formData.price}
        onChange={handleInputChange}
        variant="outlined"
        required
        InputProps={{
          startAdornment: <InputAdornment position="start">$</InputAdornment>,
          inputProps: { min: 0, step: 0.01 }
        }}
      />

      <FormControl variant="outlined" required>
        <InputLabel id="category-label">Category</InputLabel>
        <Select
          labelId="category-label"
          name="category"
          value={formData.category}
          onChange={handleInputChange}
          label="Category"
        >
          <MenuItem value="" disabled>Select a Category</MenuItem>
          {categories.map((category, index) => (
            <MenuItem key={index} value={category}>
              {category.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl variant="outlined" required>
        <InputLabel id="condition-label">Condition</InputLabel>
        <Select
          labelId="condition-label"
          name="condition"
          value={formData.condition}
          onChange={handleInputChange}
          label="Condition"
        >
          <MenuItem value="" disabled>Select a Condition</MenuItem>
          {conditions.map((condition, index) => (
            <MenuItem key={index} value={condition}>
              {condition.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl variant="outlined" required>
        <InputLabel id="location-label">Location</InputLabel>
        <Select
          labelId="location-label"
          name="location"
          value={formData.location}
          onChange={handleInputChange}
          label="Location"
        >
          <MenuItem value="" disabled>Select a Condition</MenuItem>
          {locations.map((location, index) => (
            <MenuItem key={index} value={location}>
              {location.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        label="Description"
        name="description"
        value={formData.description}
        onChange={handleInputChange}
        variant="outlined"
        multiline
        rows={4}
      />

      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </Box>
  );
}

export default CreateListing;
