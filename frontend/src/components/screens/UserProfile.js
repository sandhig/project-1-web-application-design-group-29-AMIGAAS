import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import "./UserProfile.css"
import Header from "../../components/Header"
import { Button } from '@mui/material';


function UserProfile() {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const { currentUser } = useUser();
    const token = localStorage.getItem('authToken');

    useEffect(() => {
        if (currentUser) {
            fetch(`http://3.87.240.14:8000/api/user/${userId}/`, {
                method: 'GET',
                headers: {
                  'Authorization': `Token ${token}`,
                  'Content-Type': 'application/json',
                },
              })
            .then(response => response.json())
            .then(data => setUser(data));
        }
    }, [userId, currentUser, token]);

    const handleMessageMe = () => {
        navigate(`/messages?userId=${userId}`);
    };

    const handleEditProfile = () => {
        navigate(`/profiles/edit-profile`);
    };

    return (
        <div >
            <Header />

            {!user ? (<div>Loading...</div>) : (

            <div className="profile-page-container">

                <div className="profile-info-container">

                    <div className="profile-header">

                        <div className="profile-icon">
                            {user.profilePic ? (
                                <img src={user.profilePic} alt="Profile" className="profile-pic" />
                            ) : (
                                <img src="/profile-icon.jpg" alt="Default Profile" className="profile-pic" />
                            )}
                        </div>
                        
                        <div className="profile-name">

                            <h1>{user.first_name} {user.last_name}</h1>

                            {parseInt(currentUser.id) !== parseInt(userId) && (
                                <Button onClick={handleMessageMe} variant="outlined">
                                    Send Message
                                </Button>
                            )}

                            {parseInt(currentUser.id) == parseInt(userId) && (
                                <Button onClick={handleEditProfile} variant="outlined">
                                    Edit Profile
                                </Button>
                            )}
                            
                        </div>
                        
                    </div>

                    <span style={{fontWeight:"bold", marginBottom:"10px"}}>About me</span>
                    <p>{user.bio || "This user hasn't added a bio yet."}</p>
                    
                    <span style={{fontWeight:"bold", marginBottom:"10px", marginTop:"30px"}}>Email</span>
                    <p>{user.email}</p>
                    
                </div>

                <div className="listings-info-container">
                    <h2>Listings</h2>
                </div>

            </div>
            )}
                    
        </div>
    );
}

export default UserProfile;
