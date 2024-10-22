import React from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import LogoutButton from './UsersLogOut';

function Header() {
    return (
        <header className="header">
            <div className="logo">
                <Link to="/">UofT's Too Good To Throw</Link>  
            </div>
            <nav>
                <ul className="nav-links">
                    <li><Link to="/profiles/login">Login</Link></li>   
                    <li><Link to="/users/signup">Signup</Link></li>  
                    <LogoutButton />
                    <li><Link to="/products">Products</Link></li> 
                    <li><Link to="/messages">Messages</Link></li>
                </ul>
            </nav>
        </header>   
    );
};

export default Header;