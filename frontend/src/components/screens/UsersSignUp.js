import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';



const UsersSignUp = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  });
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const isUofTEmail = (email) => {
    return email.endsWith('@mail.utoronto.ca');
  };


  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isUofTEmail(formData.email)) {
      setErrorMessage('Please use UofT Email Address.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/profiles/signup', formData, {
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
      setErrorMessage('Error adding user');
      setSuccessMessage('');
    }
  };


  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>
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
        <button type="submit">Sign Up</button>
      </form>
      <p> 
          Already User? 
          <Link to="/profiles/login"> Login</Link>
      </p>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default UsersSignUp;
