import { Button, Link, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../HeaderPre"

const EmailVerification = () => {
  const [formData, setFormData] = useState({
    email: '',
    verification_code: '',
  });

  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  const isFormInvalid = loading || Object.values(formErrors).some(error => error) || !!successMessage;

  const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@mail\.utoronto\.ca$/;
    return emailRegex.test(email) ? '' : 'Please enter a valid UofT email address.';
  };

  const validateRequired = (value) => {
    return !value ? `Please enter your verification code.` : '';
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
    } else if (name === 'verification_code') {
      errorMessage = validateRequired(value);
    }

    setFormErrors({ ...formErrors, [name]: errorMessage });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const errors = {
      email: validateEmail(formData.email),
      verification_code: validateRequired(formData.verification_code),
    };

    const hasErrors = Object.values(errors).some(error => error !== '');
    if (hasErrors) {
      setFormErrors(errors);
      return;
    }

    setLoading(true); 

    const trimmedFormData ={
      email: formData.email.trim(),
      verification_code:formData.verification_code.trim(),
    };

    try {
      const response = await axios.post('http://3.87.240.14:8000/api/profiles/verify-email', trimmedFormData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200) {
        setSuccessMessage('Email verified successfully!');
        setErrorMessage('');
        
        setTimeout(() => {
          navigate('/profiles/login');  // Redirects to verify-email page
        }, 2000);  // Adjust the timeout duration as needed
      }
    } catch (error) {
      if (error.response && error.response.data) {
        const backendErrors = error.response.data;
        const fieldErrors = {};

        // generic errors
        if (backendErrors.non_field_errors && backendErrors.non_field_errors[0]) {
            setErrorMessage(backendErrors.non_field_errors[0]);
        } 

        // form field specific errors
        Object.keys(backendErrors).forEach(key => {
          if (key !== 'non_field_errors') {
            console.log(backendErrors);
            const fieldError = backendErrors[key];

              fieldErrors[Object.keys(fieldError)] = Object.values(fieldError).map(errorArray => errorArray.join(' ')).join(' ');
          }
        });
      
      } else {
          setErrorMessage('An error occurred. Please try again.');
      }
      setSuccessMessage('');
    } finally {
      setLoading(false);  // Reset loading state when request finishes
    }
  };

  return (
    <div className="signup-page">
      <HeaderPre />
      <div className="signup-container">
        <h1>Email Verification</h1>
        <form noValidate onSubmit={handleSubmit} className='signup-form'>
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
            label="Verification Code"
            name="verification_code"
            type="text"
            value={formData.verification_code}
            onChange={handleInputChange}
            onBlur={handleBlur}
            variant="outlined"
            required
            error={!!formErrors.verification_code}
            helperText={formErrors.verification_code}
          />
            <div className='bottom-padding'>
            <Button
              name="verify"
              type="submit"
              variant="contained"
              color="primary"
              disabled={isFormInvalid}
            >
              {loading || successMessage ? 'Verifying Email...' : 'Verify Email'}
            </Button>
          </div>
        </form>
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

export default EmailVerification;
