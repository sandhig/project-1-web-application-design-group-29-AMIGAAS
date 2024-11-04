import { useUser } from '../../context/UserContext';
import React, { useState, useEffect } from 'react';
import Header from "../../components/Header"

function Wishlist() {
    
    return (
    <div>
        <Header />
        <h1>My Wishlist</h1>
    </div>
    );
}

export default Wishlist