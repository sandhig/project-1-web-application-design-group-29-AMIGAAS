import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import LogoutButton from './UsersLogOut';
import { useUser } from '../context/UserContext';

import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import MessageIcon from '@mui/icons-material/Message';
import TextField from "@mui/material/TextField";

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
      <div className="header">
        <Link to="/products">
          <img className="header-logo" src="images/logo-white.png"></img>
        </Link>
        <div className="search-container">
          <TextField
            id="search-bar"
            className="search-bar"
            onInput={(e) => {
              return;
            }}
            variant="outlined"
            placeholder="Search..."
            size="small"
          />
          <IconButton type="submit" aria-label="search">
            <SearchIcon style={{ fill: "white" }} />
          </IconButton>
        </div>
        <div className="profile-container">
          <Link to="/products/create">
              <button className="create-listing">Create Listing</button>
          </Link>
          <Link to="/messages">
            <IconButton aria-label="message">
              <MessageIcon style={{ fill: "white", fontSize: "larger" }} />
            </IconButton>
          </Link>
          <img className="header-profile" src="images/profile.png"></img>
        </div>
      </div>
    );
};

export default Header;