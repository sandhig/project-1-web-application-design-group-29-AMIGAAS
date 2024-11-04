import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navigate } from "react-router-dom";

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
import ProductListing from './components/screens/ProductListing';
import SearchResults from './components/screens/SearchResults';
import Wishlist from './components/screens/Wishlist';


function App() {

    return (
      <div className="App">
        <UserProvider>
          <Router>
            
          <div className="App-scroll-container">

            <Routes>
              {/* Public pages */}
              <Route path = "/" element={<WelcomePage/>}></Route>
              <Route path = "/profiles/signup" element={<UsersSignUp/>}></Route>
              <Route path = "/profiles/verify-email" element={<EmailVerification/>}></Route>
              <Route path = "/profiles/login" element={<UsersLogin/>}></Route>

              {/* Protected pages */}
              {/*<Route path = "/" element={<PrivateRoute element={<HomeScreen />} />}></Route>*/}
              <Route path="/" element={<Navigate to="/products" replace />} />
              <Route path="/search" element={<PrivateRoute element={<SearchResults />} />} />
              <Route path="/products" element={<PrivateRoute element={<Products />} />} />
              <Route path="/products/:id" element={<PrivateRoute element={<ProductListing />} />} />
              <Route path="/products/create" element={<PrivateRoute element={<CreateListing />} />} />
              <Route path="/user/:userId" element={<PrivateRoute element={<UserProfile />} />} />
              <Route path="/messages" element={<PrivateRoute element={<PrivateMessage />} />} />
              <Route path="/profile/:userId" element={<UserProfile />} />
              <Route path="/profiles/edit-profile" element={<EditProfile />} />
              <Route path="/wishlist" element={<Wishlist />} />
            </Routes>
    </div>
          </Router>
        </UserProvider>
      </div>
    );
  }

export default App;
