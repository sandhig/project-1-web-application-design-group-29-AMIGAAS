import React from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';  // CSS for styling
import HeaderPre from "../../components/HeaderPre"

function WelcomePage() {
    const navigate = useNavigate();

    const handleSignUp = () => {
        navigate('/profiles/signup');  // Redirect to Sign Up page
    };

    const handleLogin = () => {
        navigate('/profiles/login');  // Redirect to Log In page
    };

    return (
        <div>
            <HeaderPre />
        
            <div className="welcome-container">
                <img src="/images/welcome-page-logo-navy-2.gif" alt="Website Logo" className="welcome-logo" />
                {/* <h1 className="website-name">TooGoodToThrow</h1> */}
                <div className="button-group">
                    <button className="welcome-button" onClick={handleSignUp}>Sign Up</button>
                    <button className="welcome-button" onClick={handleLogin}>Log In</button>
                </div>
            </div>
        </div>
    );
}

export default WelcomePage;
