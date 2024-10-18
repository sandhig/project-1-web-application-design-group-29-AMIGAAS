import React from "react";
import { Route, Navigate } from "react-router-dom";
import { useUser } from '../context/UserContext';

const PrivateRoute = ({ element }) => {
  const { currentUser } = useUser();

  return currentUser ? element : <Navigate to="/users/login" />;
};

export default PrivateRoute;
