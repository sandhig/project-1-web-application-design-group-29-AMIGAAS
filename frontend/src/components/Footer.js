import React from 'react';
import './Footer.css';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function Footer() {
    const navigate = useNavigate();

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
                <Link onClick={() => navigate('/about')} style={{ marginRight: '3px' }}>About Us</Link>
                <span className='separator'>|</span>
                <Link onClick={() => navigate('/faq')} style={{ marginLeft: '3px' }}>FAQ</Link>
            </div>
        </div>
    );
}

export default Footer;


