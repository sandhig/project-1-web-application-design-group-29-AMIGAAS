import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import LogoutButton from './screens/UsersLogOut';
import { useUser } from '../context/UserContext';


import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import MessageIcon from '@mui/icons-material/Message';
import TextField from "@mui/material/TextField";
import LogoutIcon from '@mui/icons-material/Logout';

function Header() {
    const { currentUser } = useUser();
    const { setCurrentUser } = useUser();
    const [unreadMessagesCount, setUnreadMessagesCount] = useState(0);
    //const navigate = useNavigate();

    return (
        <header className="header">
            <div className="logo-container">
                <Link to="/products">
                    <img className='header-logo' src="/images/logo-white.png"></img>
                </Link>  
                <div className="site-title">Too Good To Throw</div> 
            </div>

            <nav>
                <ul className="nav-links"> 
                    <li><Link to="/products">Products</Link></li> 
                    <li><Link to="/messages">Messages</Link></li> 
                    <LogoutButton />
                    
                </ul>
            </nav>
        </header>   
    );
};

export default Header;