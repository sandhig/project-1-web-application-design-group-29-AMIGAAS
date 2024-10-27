import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import UserProfile from './components/UserProfile';
import PrivateMessage from './components/PrivateMessaging';
import Products from './components/Products';


function App() {

    return (
        <div className="App">
          <Products />
        </div>
      );

}

function HomePage({ currentUserId }) {
    const users = [
        { id: 1, name: 'User 1' },
        { id: 2, name: 'User 2' },
        { id: 3, name: 'User 3' }
    ];

    return (
        <div>
            <h1>2good2throw</h1>
            <h2>Signed in as {currentUserId}</h2>
            <h2>Users:</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        <Link to={`/user/${user.id}`}>{user.name}</Link>
                    </li>
                ))}
            </ul>
            <Link to="/messages">Messages</Link>
        </div>
    );
}

export default App;
