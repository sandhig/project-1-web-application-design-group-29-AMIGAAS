import './App.css';
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import UserProfile from './components/UserProfile';
import PrivateMessage from './components/PrivateMessaging';
import Products from "./components/screens/Products";
import UsersSignUp from "./components/screens/UsersSignUp";
import UsersLogin from './components/screens/UsersLogin';
import HomeScreen from "./components/screens/HomeScreen"; 
import EmailVerification from './components/screens/EmailVerification';
import Header from "./components/Header"; 

function App() {
    const currentUserId = 2; // Hardcoded for now

    return (
      <div className="App">
        <Router>
          <Header/>
  
          <Routes>
            <Route path = "/" element={<HomeScreen/>}></Route>
            <Route path = "/users/signup" element={<UsersSignUp/>}></Route>
            <Route path = "/users/verify-email" element={<EmailVerification/>}></Route>
            <Route path = "/users/login" element={<UsersLogin/>}></Route>
            <Route path = "/products" element={<Products/>}></Route>
            <Route path = "/user/:userId" element={<UserProfile currentUserId={currentUserId} />} />
            <Route path = "/messages" element={<PrivateMessage currentUserId={currentUserId} />} />
          </Routes>
  
        </Router>
      </div>
    );
  }

export default App;
