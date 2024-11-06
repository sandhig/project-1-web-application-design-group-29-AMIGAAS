import { Button, Link, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../components/HeaderPre"
import "./UsersSignUp.css"; 
import { useUser } from '../../context/UserContext';

const UsersLogin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  
  const [errorMessage, setErrorMessage] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate()
  const { fetchUserData } = useUser();

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

    if (name === 'email') {
      errorMessage = validateEmail(value);
    } else if (name === 'password') {
      errorMessage = validatePassword(value);
    }

    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const errors = {
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
      const response = await axios.post('http://3.87.240.14:8000/api/profiles/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200) {
        const token = response.data.token;
        localStorage.setItem('authToken', token);
        fetchUserData(token);
        
        setSuccessMessage('Login successful!');
        setErrorMessage('');
        setTimeout(() => {
          navigate('/products');  //was /homepage is not /products
        }, 2000);  

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
    <div className="signup-page">
      <HeaderPre />
      <div className='signup-container'>
        <h1>Login</h1>
        <form noValidate onSubmit={handleSubmit} className="signup-form">
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
            name="login"
            type="submit"
            variant="contained"
            color="primary"
            disabled={isFormInvalid}
          >
            {isSubmitting || successMessage ? 'Logging In...' : 'Login'}
          </Button>
        </form>
        <div className='side-by-side'>
          <div className='typography'>
            <Typography>Not a User?</Typography>
          </div>
          <div className='top-padding'>
            <Link color="primary" to="/profiles/reset">Signup</Link>
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

export default UsersLogin;
