import { Button, Link, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useSearchParams } from 'react-router-dom';
import HeaderPre from "../../HeaderPre"

const PasswordResetConfirm = () => {
    const [newPassword, setNewPassword] = useState('');
    const [searchParams] = useSearchParams();
  
    const uid = searchParams.get('uid');
    const token = searchParams.get('token');

    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [formErrors, setFormErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState('');

    const isFormInvalid = loading || Object.values(formErrors).some(error => error) || !!successMessage;

    const validatePassword = (password) => {
        if (!password) return 'Please enter a password.';
        else if (password.length < 6) return 'Password must be at least 6 characters long.'
        else return '';
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormErrors({ ...formErrors, [name]: '' });
        setNewPassword(value);
    };

    const handleBlur = (event) => {
        const { name, value } = event.target;
        let errorMessage = '';
        errorMessage = validatePassword(value);

        setFormErrors({ ...formErrors, [name]: errorMessage });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errors = {
            password: validatePassword(newPassword)
        };

        const hasErrors = Object.values(errors).some(error => error !== '');
        if (hasErrors) {
            setFormErrors(errors);
            return;
        }

        setLoading(true);

        try {
            await axios.post('http://3.87.240.14:8000/api/password_reset_confirm/', {
                uid,
                token,
                new_password: newPassword,
            });
            setSuccessMessage('Your password has been reset successfully. You can now log in with your new password.');
        } catch (err) {
            setErrorMessage('Failed to reset password. Please request a new link.');
        } finally {
            setLoading(false);  // Reset loading state when request finishes
        }
    };

    return (
        <div className="signup-page">
            <HeaderPre />
            <div className="signup-container">
                <h1>Reset Your Password</h1>
                <form noValidate onSubmit={handleSubmit} className='signup-form'>
                    <TextField
                        label="Password"
                        name="password"
                        type="password"
                        value={newPassword}
                        onChange={handleInputChange}
                        onBlur={handleBlur}
                        variant="outlined"
                        required
                        error={!!formErrors.password}
                        helperText={formErrors.password}
                    />
                    <Button
                        name="signup"
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={isFormInvalid}
                    >
                        {loading || successMessage ? 'Resetting password...' : 'Reset password'}
                    </Button>
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

export default PasswordResetConfirm;
