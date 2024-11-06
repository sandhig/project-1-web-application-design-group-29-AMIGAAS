import { Button, Link, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../components/HeaderPre"
import "./UsersSignUp.css";


const UsersSignUp = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  });

  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isFormInvalid = isSubmitting || Object.values(formErrors).some(error => error) || !!successMessage;

  const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@mail\.utoronto\.ca$/;
    return emailRegex.test(email) ? '' : 'Please enter a valid UofT email address.';
  };
  
  const validatePassword = (password) => {
    if (!password) return 'Please enter your password.';
    else if (password.length < 6) return 'Password must be at least 6 characters long.'
    else return '';
  };

  const validateRequired = (name, value) => {
    if (name === 'first_name') {
      return !value ? `Please enter your first name.` : '';
    } else if (name === 'last_name') {
      return !value ? `Please enter your last name.` : '';
    } 
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormErrors({ ...formErrors, [name]: '' });

    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleBlur = (event) => {
    const { name, value } = event.target;
    let errorMessage = '';

    if (name === 'first_name' || name === 'last_name') {
      errorMessage = validateRequired(name, value);
    } else if (name === 'email') {
      errorMessage = validateEmail(value);
    } else if (name === 'password') {
      errorMessage = validatePassword(value);
    }

    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const handleLoginButton = () => {
    navigate('/profiles/login');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const errors = {
      first_name: validateRequired('first_name', formData.first_name),
      last_name: validateRequired('last_name', formData.last_name),
      email: validateEmail(formData.email),
      password: validatePassword(formData.password),
    };

    const hasErrors = Object.values(errors).some(error => error !== '');
    if (hasErrors) {
      setFormErrors(errors);
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await axios.post('http://3.87.240.14:8000/api/profiles/signup', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 201) {
        setSuccessMessage('User successfully added!');
        setErrorMessage('');

        setTimeout(() => {
          navigate('/profiles/verify-email');  // Redirects to verify-email page
        }, 2000);  // Adjust the timeout duration as needed
      }
    } catch (error) {
      if (error.response && error.response.data) {
        const backendErrors = error.response.data;
        const fieldErrors = {};
  
        // generic errors
        if (backendErrors.non_field_errors) {
          setErrorMessage(backendErrors.non_field_errors.join(' '));
        } else {
          setErrorMessage('');
        }
  
        // form field specific errors
        Object.keys(backendErrors).forEach(key => {
          if (key !== 'non_field_errors') {
            console.log(Object.keys(backendErrors[key]));
            const fieldError = backendErrors[key];

              fieldErrors[Object.keys(fieldError)] = Object.values(fieldError).map(errorArray => errorArray.join(' ')).join(' ');
          }
        });

        setFormErrors(fieldErrors);
      } else {
        // in case of unexpected errors
        setErrorMessage('An unexpected error occurred. Please try again.');
      }

      setSuccessMessage('');
    } finally {
      setIsSubmitting(false);
    }
  };


  return (
    <div>
      <HeaderPre />
      <div className="signup-container">
        <h1>Sign Up</h1>
        <form noValidate onSubmit={handleSubmit} className="signup-form">
          <TextField
            label="First Name"
            name="first_name"
            type="text"
            value={formData.first_name}
            onChange={handleInputChange}
            onBlur={handleBlur}
            variant="outlined"
            required
            error={!!formErrors.first_name}
            helperText={formErrors.first_name}
          />
          <TextField
            label="Last Name"
            name="last_name"
            type="text"
            value={formData.last_name}
            onChange={handleInputChange}
            onBlur={handleBlur}
            variant="outlined"
            required
            error={!!formErrors.last_name}
            helperText={formErrors.last_name}
          />
          <TextField
            label="UofT Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleInputChange}
            onBlur={handleBlur}
            variant="outlined"
            required
            error={!!formErrors.email}
            helperText={formErrors.email}
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleInputChange}
            onBlur={handleBlur}
            variant="outlined"
            required
            error={!!formErrors.password}
            helperText={formErrors.password}
          />
          <Button
            name="signup"
            type="submit"
            variant="contained"
            color="primary"
            disabled={isFormInvalid}
          >
            {isSubmitting || successMessage ? 'Signing Up...' : 'Sign Up'}
          </Button>
        </form>
        <div className='side-by-side'>
          <div className='typography'>
            <Typography>Already a User?</Typography>
          </div>
          <div className='top-padding'>
            <Button
              name="signup"
              variant="text"
              color="primary"
              onClick={handleLoginButton}
            >
              <Typography color='primary'>Login</Typography>
            </Button>
          </div>
        </div>
        <div className='top-padding'>
          {errorMessage && (
            <Typography variant="body1" className="error-message">
              {errorMessage}
            </Typography>
          )}
          {successMessage && (
            <Typography variant="body1" className="success-message">
              {successMessage}
            </Typography>
          )}
        </div>
      </div>
    </div>
  );
};

export default UsersSignUp;
