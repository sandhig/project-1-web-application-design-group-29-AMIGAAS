import React, { useState, useEffect } from 'react';
import { TextField, MenuItem, Select, InputLabel, FormControl, Button, Box, InputAdornment, Typography, Alert } from '@mui/material';
import axios from 'axios';
import { useUser } from '../../context/UserContext';
import { useNavigate } from 'react-router-dom';

function CreateListing() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
    condition: '',
    location: '',
    description: '',
    image: null
  });

  const { currentUser } = useUser();
  const token = localStorage.getItem('authToken');

  const [categories, setCategories] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState(null);
  const [submitError, setSubmitError] = useState(null);
  const [formErrors, setFormErrors] = useState({});

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
      .catch(error => {
        console.error('Error fetching preset values:', error);
        setError('Failed to load preset values. Please try again later.');
      });
  }, [token]);

  const handleInputChange = (event) => {
    const { name, value, type, files } = event.target;
    setFormErrors({ ...formErrors, [name]: '' });

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

    if (type === 'file') {
      setFormData({
        ...formData,
        image: files[0]
      });
    }
  };

  const validateRequired = (event) => {
    const { name, value } = event.target;
    let errorMessage = '';
    if (!value) {
      errorMessage = `Please enter a ${name}.`;
    }
    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const validatePrice = (event) => {
    const { name, value } = event.target;
    console.log('Price:', parseFloat(value));
    let errorMessage = '';
    if (!value) {
      errorMessage = `Please enter a ${name}.`;
    } else if (parseFloat(value) >= 100000000) {
      errorMessage = 'Price must be less than $100,000,000.';
    }
    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const validateSelectField = (event) => {
    const { name, value } = event.target;
    let errorMessage = '';
    if (!value) {
      errorMessage = `Please select a ${name}.`;
    }
    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const payload = new FormData();
    payload.append('name', formData.name);
    payload.append('price', parseFloat(formData.price));
    payload.append('category', formData.category.value);
    payload.append('condition', formData.condition.value);
    payload.append('pickup_location', formData.location.value);
    payload.append('description', formData.description);
    if (formData.image) {
      payload.append('image', formData.image);
    }

    axios.post('http://3.87.240.14:8000/api/products/', payload, {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
      .then(response => {
        navigate('/products');
      })
      .catch(error => console.error('Error adding product:', error));
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      encType="multipart/form-data"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        maxWidth: 300,
        margin: 'auto'
      }}
    >
      {error && <Alert severity="error">{error}</Alert>}

      <TextField
        label="name"
        name="name"
        value={formData.name}
        onChange={handleInputChange}
        onBlur={validateRequired}
        variant="outlined"
        required
        error={!!formErrors.name}
        helperText={formErrors.name}
      />

      <TextField
        label="Price"
        name="price"
        type="number"
        value={formData.price}
        onChange={handleInputChange}
        onBlur={validatePrice}
        variant="outlined"
        required
        error={!!formErrors.price}
        helperText={formErrors.price}
        InputProps={{
          startAdornment: <InputAdornment position="start">$</InputAdornment>,
          inputProps: { min: 0, step: 0.01 }
        }}
      />

      <FormControl variant="outlined" required error={!!formErrors.category}>
        <InputLabel id="category-label">Category</InputLabel>
        <Select
          labelId="category-label"
          name="category"
          value={formData.category}
          onChange={handleInputChange}
          onBlur={validateSelectField}
          label="Category"
        >
          <MenuItem value="" disabled>Select a Category</MenuItem>
          {categories.map((category, index) => (
            <MenuItem key={index} value={category}>
              {category.label}
            </MenuItem>
          ))}
        </Select>
        <Typography variant="caption" color="error">{formErrors.category}</Typography>
      </FormControl>

      <FormControl variant="outlined" required error={!!formErrors.condition}>
        <InputLabel id="condition-label">Condition</InputLabel>
        <Select
          labelId="condition-label"
          name="condition"
          value={formData.condition}
          onChange={handleInputChange}
          onBlur={validateSelectField}
          label="Condition"
        >
          <MenuItem value="" disabled>Select a Condition</MenuItem>
          {conditions.map((condition, index) => (
            <MenuItem key={index} value={condition}>
              {condition.label}
            </MenuItem>
          ))}
        </Select>
        <Typography variant="caption" color="error">{formErrors.condition}</Typography>
      </FormControl>

      <FormControl variant="outlined" required error={!!formErrors.location}>
        <InputLabel id="location-label">Location</InputLabel>
        <Select
          labelId="location-label"
          name="location"
          value={formData.location}
          onChange={handleInputChange}
          onBlur={validateSelectField}
          label="Location"
        >
          <MenuItem value="" disabled>Select a Location</MenuItem>
          {locations.map((location, index) => (
            <MenuItem key={index} value={location}>
              {location.label}
            </MenuItem>
          ))}
        </Select>
        <Typography variant="caption" color="error">{formErrors.location}</Typography>
      </FormControl>

      <TextField
        label="Description"
        name="description"
        value={formData.description}
        onChange={handleInputChange}
        variant="outlined"
        multiline
        rows={4}
        helperText={formErrors.description}
        error={!!formErrors.description}
      />

      <input
        type="file"
        name="image"
        accept="image/*"
        onChange={handleInputChange}
      />

      {submitError && <Alert severity="error">{submitError}</Alert>}

      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </Box>
  );
}

export default CreateListing;
