import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../components/HeaderPre"
import "./UsersSignUp.css"; 

const UsersLogin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://3.87.240.14:8000/api/profiles/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200) {
        const token = response.data.token;
        localStorage.setItem('authToken', token);
        
        setSuccessMessage('Login successful!');
        setErrorMessage('');
        setTimeout(() => {
          navigate('/products');  //was /homepage is not /products
        }, 2000);  

      }
    } catch (error) {
      setErrorMessage('Invalid email or password.');
      setSuccessMessage('');
    }
  };

  return (
    <div className="signup-page">
      <HeaderPre />
      <div className='signup-container'>
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className="signup-form">
          <div>
            <label>UofT Email: </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Password: </label>
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
          <Link to="/profiles/signup"> Signup</Link>
        </p>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}
      </div>
    </div>
  );
};

export default UsersLogin;
