import './App.css';
import React from "react";
import Products from "./components/Products";
import UsersSignUp from "./components/UsersSignUp"
import UsersLogin from './components/UsersLogin';

function App() {
  return (
    <div className="App">
      <UsersSignUp />
      <UsersLogin />
      <Products />
    </div>
  );
}

export default App;
