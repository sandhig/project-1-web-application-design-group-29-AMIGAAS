import React, { useEffect, useState } from 'react';
import './Header.css'

function HeaderPre() {
    
    return (
      <div className="header">
        <div className="logo-container">
            <img className="header-logo" src="/images/logo-white.png"></img>
            <div className="site-title">Too Good To Throw</div>
        </div>
      </div>
    );
};

export default HeaderPre;