import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const EmailVerification = () => {
  const [formData, setFormData] = useState({
    email: '',
    verification_code: '',
  });

  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); 

    const trimmedFormData ={
      email: formData.email.trim(),
      verification_code:formData.verification_code.trim(),
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/profiles/verify-email', trimmedFormData, {
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
      // Improved error handling
      if (error.response && error.response.data && error.response.data.detail) {
        setErrorMessage(error.response.data.detail);
      } else {
        setErrorMessage('An error occurred. Please try again.');
      }
      setSuccessMessage('');
    } finally {
      setLoading(false);  // Reset loading state when request finishes
    }
  };

  return (
    <div>
      <h2>Email Verification</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>UofT Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Verification Code:</label>
          <input
            type="text"
            name="verification_code"
            value={formData.verification_code}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify Email'}
        </button>
      </form>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default EmailVerification;
