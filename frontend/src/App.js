import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import UserProfile from './components/UserProfile';
import PrivateMessage from './components/PrivateMessaging';
import Products from "./components/screens/Products";
import UsersSignUp from "./components/screens/UsersSignUp";
import UsersLogin from './components/screens/UsersLogin';
import HomeScreen from "./components/screens/HomeScreen"; 
import EmailVerification from './components/screens/EmailVerification';
import Header from "./components/Header"; 
import PrivateRoute from './components/PrivateRoute';

function App() {

  const [currentUserId, setCurrentUserId] = useState(null);

    useEffect(() => {
        const storedUserId = localStorage.getItem('userId');
        if (storedUserId) {
            setCurrentUserId(storedUserId);
        }
    }, []);

    return (
      <div className="App">
        <Router>
          <Header/>
  
          <Routes>
            <Route path = "/" element={<HomeScreen/>}></Route>
            <Route path = "/users/signup" element={<UsersSignUp/>}></Route>
            <Route path = "/users/verify-email" element={<EmailVerification/>}></Route>
            <Route path = "/users/login" element={<UsersLogin/>}></Route>

            {/* Protected pages */}
            <Route path="/products" element={<PrivateRoute element={<Products />} />} />
            <Route path="/user/:userId" element={<PrivateRoute element={<UserProfile currentUserId={currentUserId}/>} />} />
            <Route path="/messages" element={<PrivateRoute element={<PrivateMessage currentUserId={currentUserId}/>} />} />
          </Routes>
  
        </Router>
      </div>
    );
  }

export default App;
