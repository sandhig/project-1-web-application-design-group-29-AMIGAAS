import {
  Alert,
  Box,
  Button,
  FormControl,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  Snackbar,
  TextField,
  Typography
} from '@mui/material';
import axios from 'axios';
import React, { useState, useEffect } from 'react';

import './CreateListing.css';
import Header from "../../Header";
import { useNavigate } from 'react-router-dom';
import { useUser } from '../../../context/UserContext';

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
  const [formErrors, setFormErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [navigateAfterSnackbar, setNavigateAfterSnackbar] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const snackbarErrorMessage = "New listing was not created. Please fix the errors and try again.";
  const isFormInvalid = isSubmitting || Object.values(formErrors).some(error => error) || snackbarOpen;
  const isImageButtonDisabled = isSubmitting || snackbarOpen;

  useEffect(() => {
    axios.get('http://54.165.176.36:8000/api/product-choices/', {
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
      setSelectedImage(URL.createObjectURL(files[0]));
    }
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);

    // navigate to Products page after Snackbar closes
    if (navigateAfterSnackbar) {
      navigate('/products');
    }
  };

  const validateRequired = (name, value) => {
    return !value ? `Please enter a ${name}.` : '';
  };

  const validatePrice = (value) => {
    if (!value) return 'Please enter a valid price.';
    if (parseFloat(value) >= 100000000) return 'Price must be less than $100,000,000.';
    if (parseFloat(value) < 0) return 'Price cannot be negative.';
    return '';
  };

  const validateSelectField = (name, value) => {
    return !value ? `Please select a ${name}.` : '';
  };

  const handleBlur = (event) => {
    const { name, value } = event.target;
    let errorMessage = '';

    if (name === 'name') {
      errorMessage = validateRequired(name, value);
    } else if (name === 'price') {
      errorMessage = validatePrice(value);
    } else if (['category', 'condition', 'location'].includes(name)) {
      errorMessage = validateSelectField(name, value);
    }

    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const errors = {
      name: validateRequired('name', formData.name),
      price: validatePrice(formData.price),
      category: validateSelectField('category', formData.category),
      condition: validateSelectField('condition', formData.condition),
      location: validateSelectField('location', formData.location),
    };

    const hasErrors = Object.values(errors).some(error => error !== '');
    if (hasErrors) {
      setFormErrors(errors);
      setSnackbarMessage(snackbarErrorMessage);
      setSnackbarOpen(true);
      return;
    }

    setIsSubmitting(true);

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
    axios.post('http://54.165.176.36:8000/api/products/', payload, {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
      .then(response => {
        setSnackbarMessage("Listing Created!");
        setSnackbarOpen(true);
        setNavigateAfterSnackbar(true);
      })
      .catch(error => {
        console.error('Error adding product:', error);
        if (error.response && error.response.data) {
          const backendErrors = error.response.data;
          const fieldErrors = {};

          Object.keys(backendErrors).forEach(key => {
            fieldErrors[key] = backendErrors[key].join(' '); // if multiple messages for the same field
          });
          setFormErrors(fieldErrors);
        } else {
          setSubmitError('Failed to add product. Please check your input and try again.');
        }

        setSnackbarMessage(snackbarErrorMessage);
        setSnackbarOpen(true);
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };

  return (
    <div>
      <Header />
      <div className='padding-top'>
        <h1 className="create-listing-title">Create Listing</h1>
      </div>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit}
        encType="multipart/form-data"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          margin: 'auto'
        }}
      >
        <div className="form-container">

          <div className="create-listing-image-container">
            <img className="create-listing-image" src={selectedImage}></img>
            <input
              id="imageInput"
              type="file"
              accept="image/jpg, image/jpeg, image/webp"
              onChange={handleInputChange}
              style={{ display: 'none' }}
            />

            <p style={{ marginBottom: "10px", fontSize: "small" }}>Please upload your image in JPG, JPEG, or WEBP format.</p>

            <label htmlFor="imageInput">
              <Button
                variant="contained"
                color="primary"
                component="span"
                disabled={isImageButtonDisabled}
                sx={{
                  '&:hover': {
                    backgroundColor: '#007fa3',       // Custom hover color
                  },
                }}
              >
                Choose Image
              </Button>
            </label>

            <Typography variant="caption" color="error">{formErrors.image}</Typography>
          </div>



          <div style={{ display: "flex", flexDirection: "column", minWidth: "300px", gap: "20px", flexGrow: "1" }}>
            <div className="dropdowns">
              <TextField
                label="Name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                onBlur={handleBlur}
                variant="outlined"
                required
                error={!!formErrors.name}
                helperText={formErrors.name}
                sx={{
                  flexGrow: 1
                }}
              />

              <TextField
                label="Price"
                name="price"
                type="number"
                value={formData.price}
                onChange={handleInputChange}
                onBlur={handleBlur}
                variant="outlined"
                required
                error={!!formErrors.price}
                helperText={formErrors.price}
                InputProps={{
                  startAdornment: <InputAdornment position="start">$</InputAdornment>,
                  inputProps: { min: 0, step: 0.5 }
                }}
              />
            </div>

            <div className="dropdowns">

              <div className='align-left'>
                <FormControl variant="outlined" required error={!!formErrors.category}>
                  <InputLabel id="category-label">Category</InputLabel>
                  <Select
                    labelId="category-label"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
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
              </div>

              <div className='align-left'>
                <FormControl variant="outlined" required error={!!formErrors.condition}>
                  <InputLabel id="condition-label">Condition</InputLabel>
                  <Select
                    labelId="condition-label"
                    name="condition"
                    value={formData.condition}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
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
              </div>

              <div className='align-left'>
                <FormControl variant="outlined" required error={!!formErrors.location}>
                  <InputLabel id="location-label">Location</InputLabel>
                  <Select
                    labelId="location-label"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
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
              </div>

            </div>

            <TextField
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              multiline
              rows={4}
              variant="outlined"
            />




            <div className='submit-button'>
              <Button
                name="submit"
                type="submit"
                variant="contained"
                color="primary"
                disabled={isFormInvalid}
                sx={{
                  '&:hover': {
                    backgroundColor: '#007fa3',       // Custom hover color
                  },
                }}
              >
                {isSubmitting ? 'Submitting...' : 'Submit'}
              </Button>
            </div>
          </div>
        </div>


        {submitError && <Alert severity="error">{submitError}</Alert>}
        {error && <Alert severity="error">{error}</Alert>}

        <Snackbar
          open={snackbarOpen}
          autoHideDuration={3000}
          onClose={handleSnackbarClose}
          message={snackbarMessage}
        />
      </Box>
    </div>
  );
}

export default CreateListing;
