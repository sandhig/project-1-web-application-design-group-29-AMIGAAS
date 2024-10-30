import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import LogoutButton from './screens/UsersLogOut';
import { useUser } from '../context/UserContext';

function Header() {
    const { currentUser } = useUser();
    const [unreadMessagesCount, setUnreadMessagesCount] = useState(0);
    
    return (
        <header className="header">
            <div className="logo">
                <Link to="/homepage">UofT's Too Good To Throw</Link>  
            </div>
            <nav>
                <ul className="nav-links">
                    <li><Link to="/profiles/login">Login</Link></li>   
                    <li><Link to="/profiles/signup">Signup</Link></li>  
                    <li><Link to="/products">Products</Link></li> 
                    <li><Link to="/messages">Messages</Link></li> 
                    <LogoutButton />
                    
                </ul>
            </nav>
        </header>   
    );
};

export default Header;