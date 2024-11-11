import { Button, Link, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeaderPre from "../../HeaderPre"

const PasswordReset = () => {
    const [email, setEmail] = useState('');

    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [formErrors, setFormErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState('');

    const isFormInvalid = loading || Object.values(formErrors).some(error => error) || !!successMessage;

    const validateEmail = (email) => {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@mail\.utoronto\.ca$/;
        return emailRegex.test(email) ? '' : 'Please enter a valid UofT email address.';
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormErrors({ ...formErrors, [name]: '' });
        setEmail(value);
    };

    const handleBlur = (event) => {
        const { name, value } = event.target;
        let errorMessage = '';
        errorMessage = validateEmail(value);

        setFormErrors({ ...formErrors, [name]: errorMessage });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errors = {
            email: validateEmail(email)
        };

        const hasErrors = Object.values(errors).some(error => error !== '');
        if (hasErrors) {
            setFormErrors(errors);
            return;
        }

        setLoading(true);

        try {
            const response = await axios.post('http://54.165.176.36:8000/api/password_reset_request/', { email });
            setSuccessMessage('If this email is registered, a password reset link will be sent shortly. This may take a few minutes.');
        } catch (err) {
            setErrorMessage('An error occurred. Please try again.');
        } finally {
            setLoading(false);  // Reset loading state when request finishes
        }
    };

    return (
        <div className="signup-page">
            <HeaderPre />
            <div className="signup-container">
                <h1>Forgot Password</h1>
                <form noValidate onSubmit={handleSubmit} className='signup-form'>
                    <TextField
                        label="UofT Email"
                        name="email"
                        type="email"
                        value={email}
                        onChange={handleInputChange}
                        onBlur={handleBlur}
                        variant="outlined"
                        required
                        error={!!formErrors.email}
                        helperText={formErrors.email}
                    />
                    <div className='bottom-padding'>
                        <Button
                            name="verify"
                            type="submit"
                            variant="contained"
                            color="primary"
                            disabled={isFormInvalid}
                            sx={{
                                '&:hover': {
                                backgroundColor: '#007fa3',       // Custom hover color
                                },
                            }}
                        >
                            {loading || successMessage ? 'Sending link...' : 'Send me a link'}
                        </Button>
                    </div>
                </form>
                <div className='top-padding'>
                    {errorMessage && (
                        <Typography variant="body1" className="error-message">
                            {errorMessage}
                        </Typography>
                    )}
                    {successMessage && (
                        <Typography variant="body1" className="success-message">
                            {successMessage}
                        </Typography>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PasswordReset;
