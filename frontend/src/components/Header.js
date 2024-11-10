import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import './Header.css'
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import MessageIcon from '@mui/icons-material/Message';
import TextField from "@mui/material/TextField";
import LogoutIcon from '@mui/icons-material/Logout';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';

function Header() {
  const { currentUser, logout } = useUser();
  const [unreadMessagesCount, setUnreadMessagesCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();
  const isUnmounting = useRef(false);
  const ws = useRef(null);

  useEffect(() => {
  }, [currentUser]);

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearch = () => {
    navigate(`/search?query=${searchTerm}`);
  };

  const handleCategorySelect = (category) => {
    navigate(`/category?query=${category}`);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/profiles/login');
  };

  useEffect(() => {
    const token = localStorage.getItem('authToken');

    const fetchUnreadMessageCount = async () => {
      try {
        const response = await fetch('http://54.165.176.36:8000/api/unread_messages/', {
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

    if (currentUser && token) {
      fetchUnreadMessageCount();

      ws.current = new WebSocket(`ws://54.165.176.36:8000/ws/chat/user/${currentUser.id}/`);

      ws.current.onopen = function () {
        console.log("WebSocket connection opened");
      };

      ws.current.onmessage = function () {
        fetchUnreadMessageCount();
      };

      ws.current.onclose = function () {
        console.log("WebSocket connection closed");
      };

      ws.current.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      return () => {
        if (ws.current) {
          ws.current.close();
        }
      };
    }
  }, [currentUser]);

  return (
    <div className="header-container">

      <div className="header">

        <div className="logo-container">
          <Link to="/products" style={{display:'flex', alignItems:'center', gap:'20px'}}>
            <img className="header-logo" src="/images/header-logo-navy-cyan-white.png" alt="Website Logo"></img>
            <div className="site-title">TOO GOOD TO THROW</div>
          </Link>
        </div>

        <div className="search-container">
          <TextField
            id="search-bar"
            className="search-bar"
            onInput={handleInputChange}
            onKeyPress={handleKeyPress}
            variant="outlined"
            placeholder="Search..."
            size="small"
          />
          <IconButton type="submit" aria-label="search" onClick={handleSearch}>
            <SearchIcon className="search-icon" />
          </IconButton>
        </div>

        <div className="profile-container">

          <Link to="/products/create" className="icon-button">
            <IconButton aria-label="message">
              <AddCircleOutlineIcon className="icon" />
            </IconButton>
            <p>New Listing</p>
          </Link>

          <Link to="/messages" className="icon-button">
            <div className="message-button-container">
              <IconButton aria-label="message">
                <MessageIcon className="icon" />
              </IconButton>
              {unreadMessagesCount > 0 && (
                <span className="bubble">{unreadMessagesCount}</span>
              )}
            </div>
            <p>Messages</p>
          </Link>

          <Link to="/wishlist" className="icon-button">
            <IconButton aria-label="message">
              <FavoriteIcon className="icon" />
            </IconButton>
            <p>My Wishlist</p>
          </Link>

          <div className="icon-button">
            <IconButton aria-label="message" onClick={handleLogout}>
              <LogoutIcon className="icon" />
            </IconButton>
            <p>Logout</p>
          </div>

          {currentUser ? (
            <Link to={`/user/${currentUser.id}`} style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
              <p style={{ color: "white" }}>Hi, {currentUser.first_name}</p>
              {currentUser.profilePic ? (
                <img src={currentUser.profilePic} alt="Profile" className="header-profile" />
              ) : (
                <img src="/profile-icon.jpg" alt="Default Profile" className="header-profile" />
              )}
            </Link>
          ) : null}

        </div>

      </div>

      <div className="header-categories">
        <h2></h2>
        <h2 onClick={() => handleCategorySelect('textbook')}>Textbooks</h2>
        <h2 onClick={() => handleCategorySelect('clothing')}>Clothing</h2>
        <h2 onClick={() => handleCategorySelect('furniture')}>Furniture</h2>
        <h2 onClick={() => handleCategorySelect('electronics')}>Electronics</h2>
        <h2 onClick={() => handleCategorySelect('stationary')}>Stationary</h2>
        <h2 onClick={() => handleCategorySelect('miscellaneous')}>Miscellaneous</h2>
        <h2></h2>
      </div>
    </div>
  );
};

export default Header;