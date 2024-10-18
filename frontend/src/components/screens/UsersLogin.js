import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const UsersLogin = () => {
  const [formData, setFormData] = useState({
    uoft_email: '',
    password: '',
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
      const response = await axios.post('http://127.0.0.1:8000/api/users/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200) {
        const token = response.data.token;
        const userId = response.data.user_id;
        localStorage.setItem('authToken', token);
        localStorage.setItem('userId', userId);
        
        setSuccessMessage('Login successful!');
        setErrorMessage('');
        // Optionally, you could store a token or session data here
      }
    } catch (error) {
      setErrorMessage('Invalid email or password.');
      setSuccessMessage('');
    }
  };

  return (
    <div>
      <h2>Login</h2>
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
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>

      <p> 
          Not a User? 
          <Link to="/users/signup"> Signup</Link>
      </p>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default UsersLogin;
