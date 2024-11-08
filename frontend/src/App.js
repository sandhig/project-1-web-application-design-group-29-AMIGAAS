import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navigate } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';

import UserProfile from './components/screens/profiles/UserProfile';
import PrivateMessage from './components/screens/PrivateMessaging';
import Products from './components/screens/products/Products';
import CreateListing from './components/screens/products/CreateListing';
import UsersSignUp from "./components/screens/profiles/UsersSignUp";
import UsersLogin from './components/screens/profiles/UsersLogin';
import EmailVerification from './components/screens/profiles/EmailVerification';
import PrivateRoute from './components/PrivateRoute';
import { UserProvider } from './context/UserContext';
import WelcomePage from './components/screens/WelcomePage';
import EditProfile from './components/screens/products/EditProfile';
import ProductListing from './components/screens/products/ProductListing';
import SearchResults from './components/screens/products/SearchResults';
import Wishlist from './components/screens/products/Wishlist';
import CategoryPage from './components/screens/products/CategoryPage';
import PasswordReset from './components/screens/profiles/PasswordReset';
import PasswordResetConfirm from './components/screens/profiles/PasswordResetConfirm';

const theme = createTheme({
  palette: {
    primary: {
      main: '#001f3f', // header navy blue
    },
  },
});

function App() {

    return (
      <div className="App">
        <ThemeProvider theme={theme}>
          <UserProvider>
            <Router>
              
            <div className="App-scroll-container">
              <Routes>
                {/* Public pages */}
                <Route path = "/" element={<WelcomePage/>}></Route>
                <Route path = "/profiles/signup" element={<UsersSignUp/>}></Route>
                <Route path = "/profiles/verify-email" element={<EmailVerification/>}></Route>
                <Route path = "/password_reset_request" element={<PasswordReset/>}></Route>
                <Route path = "/password_reset_confirm" element={<PasswordResetConfirm/>}></Route>
                <Route path = "/profiles/login" element={<UsersLogin/>}></Route>

                {/* Protected pages */}
                <Route path="/" element={<Navigate to="/products" replace />} />
                <Route path="/search" element={<PrivateRoute element={<SearchResults />} />} />
                <Route path="/category" element={<PrivateRoute element={<CategoryPage />} />} />
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
        </ThemeProvider>
      </div>
    );
  }

export default App;
