import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUserData = (token) => {
    fetch('http://54.165.176.36:8000/api/profiles/get_user', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        if (!response.ok) throw new Error('Failed to fetch user data');
        return response.json();
      })
      .then(data => {
        setCurrentUser({
          id: data.id,
          profile_id: data.profile_id,
          username: data.username,
          email: data.email,
          first_name: data.first_name,
          last_name: data.last_name,
          profilePic: data.profile_pic,
          token: token,
        });
      })
      .catch(error => {
        console.error("Error fetching user data:", error);
        setCurrentUser(null);
      })
      .finally(() => setLoading(false));
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setCurrentUser(null);
  };

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token && token !== 'undefined') {
      fetchUserData(token);
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <UserContext.Provider value={{ currentUser, setCurrentUser, fetchUserData, logout }}>
      {!loading && children}
    </UserContext.Provider>
  );
};
