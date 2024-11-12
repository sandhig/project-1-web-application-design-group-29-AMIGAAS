import React, { useEffect, useState } from 'react';
import './ProductListing.css';
import {
    Alert,
    Box,
    Button,
    Checkbox,
    FormControl,
    FormControlLabel,
    InputAdornment,
    InputLabel,
    MenuItem,
    Select,
    Snackbar,
    TextField,
    Typography
  } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ProductEdit = ({
        product, 
        currentUser
    }) => {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        name: product.name,
        price: product.price,
        category: null,
        condition: null,
        location: null,
        description: product.description,
        image: product.image,
        sold: product.sold
    });

    const token = localStorage.getItem('authToken');
    const [selectedImage, setSelectedImage] = useState(product.image || null);

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

            setFormData({
                ...formData,
                category: categories.find(cat => cat.value === product.category),
                condition: conditions.find(cond => cond.value === product.condition),
                location: locations.find(loc => loc.value === product.pickup_location)
            });
          })
          .catch(error => console.error('Error fetching preset values:', error));
    }, []);

    const handleInputChange = (event) => {
        const { name, value, type, files, checked } = event.target;
        setFormErrors({ ...formErrors, [name]: '' });

        if (type === 'checkbox') {
            setFormData({
                ...formData,
                [name]: checked
            });
        } else if (name === 'price') {
            const validPrice = value.match(/^\d*(\.\d{0,2})?$/);
            if (validPrice) {
                setFormData({
                    ...formData,
                    [name]: value
                });
            }
        } else if (type === 'file') {
            const file = files[0];

            if (!file) {
                return;
            }

            // Check if the file type is JPEG
            if (file && !file.type.includes('jpeg') && !file.name.endsWith('.jpg')) {
                setFormErrors({
                    ...formErrors,
                    image: 'Please upload a .jpg or .jpeg file'
                });
                setSnackbarMessage("Invalid image format. Please upload a .jpg or .jpeg file.");
                setSnackbarOpen(true);
                setFormData({
                    ...formData,
                    image: null
                });
                return;
            }

            setFormData({ ...formData, image: file });
            setSelectedImage(URL.createObjectURL(file));
        } else {
            setFormData({
                ...formData,
                [name]: value
            });
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
        payload.append('sold', formData.sold)

        if (formData.image instanceof File) {
            payload.append('image', formData.image);
        }
        axios.put(`http://54.165.176.36:8000/api/products/${product.id}/`, payload, {
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            setSnackbarMessage("Listing updated successfully!");
            setSnackbarOpen(true);
            setNavigateAfterSnackbar(true);
        })
        .catch(error => {
            console.error('Error updating product:', error);
            if (error.response && error.response.data) {
                const backendErrors = error.response.data;
                const fieldErrors = {};

                Object.keys(backendErrors).forEach(key => {
                    if (!fieldErrors[key]) {
                        setSubmitError(backendErrors[key]);
                    } else {
                        fieldErrors[key] = backendErrors[key].join(' '); // Handle multiple error messages for the same field
                    }
                });

                setFormErrors(fieldErrors); 
            } else {
                setSubmitError('Failed to update product. Please check your input and try again.');
            }

        setSnackbarMessage(snackbarErrorMessage);
        setSnackbarOpen(true);
        })
        .finally(() => {
            setIsSubmitting(false);
        });
    };
    
    return (
        <>
        {product ? (
            <Box
                component="form"
                noValidate
                onSubmit={handleSubmit}
                encType="multipart/form-data"
                className="listing-container"
            >
                <div className="listing-image-container">
                    <img className="listing-image" src={selectedImage}></img>
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
            
                </div>

                <span className="listing-details">
                    <div>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    name="sold"
                                    checked={Boolean(formData.sold)}
                                    onChange={handleInputChange}
                                />
                            }
                            label="Mark as sold"
                        />
                    </div>

                    <div className="listing-header">
                        <TextField
                            className="listing-title"
                            label="Name"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            variant="outlined"
                            required
                            error={!!formErrors.name}
                            helperText={formErrors.name}
                        />
                    </div>

                    <TextField
                        className="listing-price"
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

                    <h2 style={{margin: "0"}}>Product details</h2>

                    <TextField
                        className="listing-description"
                        label="Description"
                        name="description"
                        value={formData.description}
                        onChange={handleInputChange}
                        multiline
                        rows={4}
                        variant="outlined"
                    />

                    <div className='align-left'> 
                        <FormControl variant="outlined" required error={!!formErrors.category}>
                            <InputLabel id="category-label" shrink>Category</InputLabel>
                            <Select
                            labelId="category-label"
                            name="category"
                            value={formData.category || ""}
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
                            <InputLabel id="condition-label" shrink>Condition</InputLabel>
                            <Select
                            labelId="condition-label"
                            name="condition"
                            value={formData.condition || ""}
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
                            <InputLabel id="location-label" shrink>Location</InputLabel>
                            <Select
                            labelId="location-label"
                            name="location"
                            value={formData.location || ""}
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
                        {isSubmitting ? 'Saving changes...' : 'Save changes'}
                    </Button>

                    {submitError && <Alert severity="error">{submitError}</Alert>}
                    {error && <Alert severity="error">{error}</Alert>}

                    <Snackbar
                        open={snackbarOpen}
                        autoHideDuration={3000}
                        onClose={handleSnackbarClose}
                        message={snackbarMessage}
                    />

                </span>
                
            </Box>
        ) : (
            <p>No product info</p>
        )}
        </>
    )
} 

export default ProductEdit;