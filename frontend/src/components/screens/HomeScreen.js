import { useUser } from '../../context/UserContext';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from "../../components/Header"

function HomeScreen() {
    const { currentUser } = useUser();
    const [profiles, setProfiles] = useState([]);

    useEffect(() => {
      const token = localStorage.getItem('authToken');
    
      fetch('http://3.87.240.14:8000/api/profiles/', {
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
    }, [currentUser]);

    if (!currentUser) {
        return <p>Loading...</p>;
      }
    
      return (
        <div>
          <Header />
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