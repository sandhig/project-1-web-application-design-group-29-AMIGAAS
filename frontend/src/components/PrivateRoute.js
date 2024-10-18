import React from "react";
import { Route, Navigate } from "react-router-dom";

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem('authToken');

  return token && token !== 'undefined' ? element : <Navigate to="/users/login" />;
};

export default PrivateRoute;
