import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export const useUser = () => {
  return useContext(UserContext);
};

export const UserProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
  
    useEffect(() => {
      const token = localStorage.getItem('authToken');

      if (token && token !== 'undefined') {
        fetch('http://localhost:8000/api/users/get_user', {
            method: 'GET',
            headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
              throw new Error('Failed to fetch user data');
            }
            return response.json();
        })
        .then(data => {
            setCurrentUser({
                ...data,
                token: token
            });
        })
        .catch(error => {
          console.error("Error fetching user data", error);
        });
      }
    }, []);

    return (
    <UserContext.Provider value={{ currentUser, setCurrentUser }}>
        {children}
    </UserContext.Provider>
    );
};