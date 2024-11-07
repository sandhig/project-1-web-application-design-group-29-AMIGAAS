import React, { useEffect, useState } from 'react';
import './Header.css'

function HeaderPre() {
    
    return (
      <div className="header">
        <div className="logo-container">
            <img className="header-logo" src="/images/header-logo-navy-cyan-white.png" alt="Website logo"></img>
            <div className="site-title">TOO GOOD TO THROW</div>
        </div>
      </div>
    );
};

export default HeaderPre;