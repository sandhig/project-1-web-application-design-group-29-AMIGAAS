import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import LogoutButton from './UsersLogOut';
import { useUser } from '../context/UserContext';

function Header() {
    const { currentUser } = useUser();
    const [unreadMessagesCount, setUnreadMessagesCount] = useState(0);
    /*
    useEffect(() => {
        const token = localStorage.getItem('authToken');
        
        if (currentUser && token) {
            const fetchUnreadMessagesCount = async () => {
                try {
                const response = await fetch('http://3.87.240.14:8000/api/unread_messages/', {
                    headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();
                setUnreadMessagesCount(data.unread_message_count);
                } catch (error) {
                console.error("Error fetching unread messages count:", error);
                }
            };

            fetchUnreadMessagesCount();
            const intervalId = setInterval(fetchUnreadMessagesCount, 30000);
            return () => clearInterval(intervalId);
        }
    }, [currentUser]);
    */
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
                    {/*
                    <li><Link to="/messages">
                    {unreadMessagesCount > 0? (
                        <div className="messages-title">
                            Messages
                            <span className="bubble">{unreadMessagesCount}</span>
                        </div>
                    ) : (<div>Messages</div>)}
                    </Link></li>
                    */}
                </ul>
            </nav>
        </header>   
    );
};

export default Header;