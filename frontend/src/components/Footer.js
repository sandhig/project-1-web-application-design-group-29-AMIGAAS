import React from 'react';
import './Footer.css'

function Footer() {

  return (
    <div className="footer-container">
        <div className="company-info">
            <p>&copy; 2024 Too Good to Throw - AMIGAAS | University of Toronto | Group 29</p>
        </div>
        <div className="contact-info">
            <p>Contact us at: <a href="mailto:toogoodtothrow59@gmail.com">toogoodtothrow59@gmail.com</a></p>
            <p>27 King's College Circle, Toronto, ON</p>
            <p>(416) 978-2011</p>
        </div>
        <div className="mission-statement">
            <p>Connecting students with affordable, second-hand goods.</p>
        </div>
        <div className="social-icons">
            <span className="icon">📷</span>
            <span className="icon">📘</span>
            <span className="icon">💼</span>
            <span className="icon">🐦</span>
        </div>
        <div className="policies">
            <p>Privacy Policy | Terms of Service | Refund Policy</p>
        </div>
        <div className="university-notice">
            <p>This is a student project for educational purposes under the ECE444 course at the University of Toronto.</p>
        </div>
    </div>
  );
};

export default Footer;