import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import './Header.css'
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import MessageIcon from '@mui/icons-material/Message';
import TextField from "@mui/material/TextField";
import LogoutIcon from '@mui/icons-material/Logout';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';

function Header() {
    const { currentUser } = useUser();
    const { setCurrentUser } = useUser();
    const [unreadMessagesCount, setUnreadMessagesCount] = useState(0);
    const [searchTerm, setSearchTerm] = useState("");
    const navigate = useNavigate();

    const handleInputChange = (e) => {
      setSearchTerm(e.target.value);
    };
  
    const handleSearch = () => {
      navigate(`/search?query=${searchTerm}`);
    };

    const handleKeyPress = (e) => {
      if (e.key === "Enter") {
        handleSearch();
      }
    };

    const handleLogout = () => {
      localStorage.removeItem('authToken');
      setCurrentUser(null);
      navigate('/profiles/login');
    };
    
    return (
      <div className="header">
        <div className="logo-container">
          <Link to="/products" style={{display:'flex', alignItems:'center', gap:'20px'}}>
            <img className="header-logo" src="/images/logo-white.png"></img>
            <div className="site-title">Too Good To Throw</div>
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
            <SearchIcon style={{ fill: "white" }} />
          </IconButton>
        </div>
        <div className="profile-container">
          <Link to="/products/create" className="icon-button">
            <IconButton aria-label="message">
              <AddCircleOutlineIcon style={{ fill: "white", fontSize: "larger" }} />
            </IconButton>
            <p>New Listing</p>
          </Link>
          <Link to="/messages" className="icon-button">
            <IconButton aria-label="message">
              <MessageIcon style={{ fill: "white", fontSize: "larger" }} />
            </IconButton>
            <p>Messages</p>
          </Link>
          <div className="icon-button">
            <IconButton aria-label="message" onClick={handleLogout}>
              <LogoutIcon style={{ fill: "white", fontSize: "larger" }} />
            </IconButton>
            <p>Logout</p>
          </div>
          {currentUser ? (
            <Link to={`/user/${currentUser.id}`} style={{display:'flex', alignItems:'center', gap:'10px', cursor:'pointer'}}>
              <p style={{color: "white"}}>Hi, {currentUser.first_name}</p>
              {currentUser.profilePic ? (
                <img src={currentUser.profilePic} alt="Profile" className="header-profile"/>
                ) : (
                <img src="/profile-icon.jpg" alt="Default Profile" className="header-profile" />
                )}
            </Link>
          ) : null}
        </div>
      </div>
    );
};

export default Header;