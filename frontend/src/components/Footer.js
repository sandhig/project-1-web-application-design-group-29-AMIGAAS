/* Footer.js */

import React from 'react';
import './Footer.css';
import { Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';


function Footer() {

    const location = useLocation();
    // List of routes where the footer should NOT be displayed
    const hiddenFooterPaths = ['/profiles/login', '/profiles/verify-email', '/password_reset_request', '/password_reset_confirm', '/profiles/signup', '/', '/messages'];

    // Footer on certain pages don't render
    if (hiddenFooterPaths.includes(location.pathname)) {
        return null;
    }
    
    return (
        <div className="footer-container">
            <div className="company-info">
                <p>&copy; 2024 Too Good to Throw - AMIGAAS | University of Toronto | Group 29</p>
            </div>
            <div className="contact-info">
                <p>Contact us at: <a href="mailto:toogoodtothrow59@gmail.com">toogoodtothrow59@gmail.com</a></p>
            </div>
            <div className="footer-links">
                {/* About and FAQ buttons */}
                <Link to='/about' style={{ marginRight: '3px' }}>About Us</Link>
                <span className='separator'>|</span>
                <Link to='/faq' style={{ marginLeft: '3px' }}>FAQ</Link>
            </div>
        </div>
    );
}

export default Footer;