import './App.css';
import React from "react";
import Products from "./components/screens/Products";
import UsersSignUp from "./components/screens/UsersSignUp";
import UsersLogin from './components/screens/UsersLogin';
import HomeScreen from "./components/screens/HomeScreen"; 
import EmailVerification from './components/screens/EmailVerification';
import Header from "./components/Header"; 

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <Router>
        <Header/>

        <Routes>
          <Route path = "/" element={<HomeScreen/>}></Route>
        </Routes>

        <Routes>
          <Route path = "/users/signup" element={<UsersSignUp/>}></Route>
        </Routes>

        <Routes>
          <Route path = "/users/verify-email" element={<EmailVerification/>}></Route>
        </Routes>

        <Routes>
          <Route path = "/users/login" element={<UsersLogin/>}></Route>
        </Routes>

        <Routes>
          <Route path = "/products" element={<Products/>}></Route>
        </Routes>

      </Router>
    </div>
  );
}

export default App;
