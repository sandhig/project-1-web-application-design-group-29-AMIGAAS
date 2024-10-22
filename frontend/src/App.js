import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import UserProfile from './components/UserProfile';
import PrivateMessage from './components/PrivateMessaging';
import Products from './components/Products';
import CreateListing from './components/CreateListing';

function App() {
    const currentUserId = 1; // Hardcoded for now

    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage currentUserId={currentUserId} />} />
                <Route path="/user/:userId" element={<UserProfile currentUserId={currentUserId} />} />
                <Route path="/products" element={<Products />} />
                <Route path="/products/create" element={<CreateListing />} />
                <Route path="/messages" element={<PrivateMessage currentUserId={currentUserId} />} />
            </Routes>
        </Router>
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
            <p>
                <Link to="/products">Products</Link>
            </p>
            <p>
                <Link to="/messages">Messages</Link>
            </p>
        </div>
    );
}

export default App;
