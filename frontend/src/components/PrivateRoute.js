import React from "react";
import { Route, Navigate } from "react-router-dom";

const isAuthenticated = () => {
    return localStorage.getItem("authToken") !== null;
};

const PrivateRoute = ({ element, ...rest }) => {
    return isAuthenticated() ? element : <Navigate to="/users/login" />;
};

export default PrivateRoute;
