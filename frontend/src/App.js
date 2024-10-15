import './App.css';
import React from "react";
import Products from "./components/Products";
import Users from "./components/Users"

function App() {
  return (
    <div className="App">
      <Users />
      <Products />
    </div>
  );
}

export default App;
