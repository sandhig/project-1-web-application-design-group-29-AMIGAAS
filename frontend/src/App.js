import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import UserProfile from './components/screens/UserProfile';
import PrivateMessage from './components/screens/PrivateMessaging';
import Products from './components/screens/Products';
import CreateListing from './components/screens/CreateListing';
import UsersSignUp from "./components/screens/UsersSignUp";
import UsersLogin from './components/screens/UsersLogin';
import HomeScreen from "./components/screens/HomeScreen"; 
import EmailVerification from './components/screens/EmailVerification';
import Header from "./components/Header"; 
import PrivateRoute from './components/PrivateRoute';
import { UserProvider } from './context/UserContext';
import WelcomePage from './components/screens/WelcomePage';
import EditProfile from './components/screens/EditProfile';

function App() {

    return (
      <div className="App">
        <UserProvider>
          <Router>
            {/*<Header/>*/}
    
            <Routes>
              {/* Public pages */}
              <Route path = "/" element={<WelcomePage/>}></Route>
              <Route path = "/profiles/signup" element={<UsersSignUp/>}></Route>
              <Route path = "/profiles/verify-email" element={<EmailVerification/>}></Route>
              <Route path = "/profiles/login" element={<UsersLogin/>}></Route>

              {/* Protected pages */}
              <Route path ="/homepage" element={<PrivateRoute element={<HomeScreen />} />}></Route>
              <Route path="/products" element={<PrivateRoute element={<Products />} />} />
              <Route path="/products/create" element={<PrivateRoute element={<CreateListing />} />} />
              <Route path="/user/:userId" element={<PrivateRoute element={<UserProfile />} />} />
              <Route path="/messages" element={<PrivateRoute element={<PrivateMessage />} />} />
              <Route path="/profile/:userId" element={<UserProfile />} />
              <Route path="/profiles/edit-profile" element={<EditProfile />} />
            </Routes>
    
          </Router>
        </UserProvider>
      </div>
    );
  }

export default App;
