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
import { UserProvider } from './context/UserContext';

function App() {

    return (
      <div className="App">
        <UserProvider>
          <Router>
            <Header/>
    
            <Routes>
              {/* Public pages */}
              <Route path = "/users/signup" element={<UsersSignUp/>}></Route>
              <Route path = "/users/verify-email" element={<EmailVerification/>}></Route>
              <Route path = "/profiles/login" element={<UsersLogin/>}></Route>

              {/* Protected pages */}
              <Route path = "/" element={<PrivateRoute element={<HomeScreen />} />}></Route>
              <Route path="/products" element={<PrivateRoute element={<Products />} />} />
              <Route path="/user/:userId" element={<PrivateRoute element={<UserProfile />} />} />
              <Route path="/messages" element={<PrivateRoute element={<PrivateMessage />} />} />
            </Routes>
    
          </Router>
        </UserProvider>
      </div>
    );
  }

export default App;
