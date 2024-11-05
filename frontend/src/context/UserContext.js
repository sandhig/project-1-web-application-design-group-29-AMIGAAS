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
        fetch('http://3.87.240.14:8000/api/profiles/get_user', {
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