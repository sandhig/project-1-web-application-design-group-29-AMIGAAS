import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../components/HeaderPre"
import { useUser } from '../../context/UserContext';


const UsersLogin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate()
  const { fetchUserData } = useUser();

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
        fetchUserData(token);
        
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
    <div>
      <HeaderPre />
      <h2>Login</h2>
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
          <Link to="/profiles/signup"> Signup</Link>
      </p>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default UsersLogin;
