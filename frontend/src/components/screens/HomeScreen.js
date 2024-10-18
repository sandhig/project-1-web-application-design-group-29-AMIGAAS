import React from 'react';
import { useUser } from '../../context/UserContext';

function HomeScreen() {
    const { currentUser } = useUser();

    if (!currentUser) {
        return <p>No user is logged in</p>;
      }
    
      return (
        <div>
          <h1>Welcome, {currentUser.first_name}!</h1>
        </div>
      );
}

export default HomeScreen