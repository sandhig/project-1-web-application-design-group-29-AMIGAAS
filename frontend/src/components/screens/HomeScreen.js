import { useUser } from '../../context/UserContext';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function HomeScreen() {
    const { currentUser } = useUser();
    const [profiles, setProfiles] = useState([]);

    useEffect(() => {
      const token = localStorage.getItem('authToken');
    
      fetch('http://localhost:8000/api/profiles/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch profiles');
        }
        return response.json();
      })
      .then((data) => {
        setProfiles(data);
      })
    }, []);

    if (!currentUser) {
        return <p>Loading...</p>;
      }
    
      return (
        <div>
          <h1>Welcome, {currentUser.first_name}!</h1>
          <h2>Users:</h2>
          <ul>
              {profiles.map(profile => (
                  <li key={profile.user_id}>
                      <Link to={`/user/${profile.user_id}`}>{profile.first_name} {profile.last_name}</Link>
                  </li>
              ))}
          </ul>
        </div>
      );
}

export default HomeScreen