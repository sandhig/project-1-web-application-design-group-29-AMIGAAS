import {Button, Stack} from '@mui/material';
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
                
                <Stack direction="row" spacing={2}>
                    <Button
                        name="signup-button"
                        variant="contained"
                        onClick={handleSignUp}
                        sx={{
                            backgroundColor: '#00204E',         // Default color
                            '&:hover': {
                            backgroundColor: '#007fa3',       // Custom hover color
                            },
                        }}
                    >
                        Sign Up
                    </Button>
                    <Button
                        name="login-button"
                        variant="contained"
                        onClick={handleLogin}
                        sx={{
                            backgroundColor: '#00204E',         // Default color
                            '&:hover': {
                            backgroundColor: '#007fa3',       // Custom hover color
                            },
                        }}
                    >
                        Log In
                    </Button>
                </Stack>
            </div>
        </div>
    );
}

export default WelcomePage;
