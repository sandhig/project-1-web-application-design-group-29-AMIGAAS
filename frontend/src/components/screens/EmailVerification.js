import React, { useState } from 'react';
import axios from 'axios';

const EmailVerification = () => {
  const [formData, setFormData] = useState({
    uoft_email: '',
    verification_code: '',
  });

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
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/users/verify-email/', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200) {
        setSuccessMessage('Email verified successfully!');
        setErrorMessage('');
      }
    } catch (error) {
      setErrorMessage('Invalid verification code or email.');
      setSuccessMessage('');
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
            name="uoft_email"
            value={formData.uoft_email}
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
        <button type="submit">Verify Email</button>
      </form>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default EmailVerification;
