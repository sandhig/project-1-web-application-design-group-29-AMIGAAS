import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import "./UserProfile.css"
import Header from "../../components/Header"


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

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div >
            <Header />
        
        <div className="profile-container-1">
            
            <div className="profile-header">
            
                <div className="profile-icon">
                    {user.profilePic ? (
                        <img src={user.profilePic} alt="Profile" className="profile-pic" />
                    ) : (
                        <img src="/profile-icon.jpg" alt="Default Profile" className="profile-pic" />
                    )}
                </div>
                <div className="profile-info">
                    <h2>{user.first_name} {user.last_name}</h2>
                    <p>{user.email}</p>
                </div>
            </div>

            <div className="profile-bio">
                <h3>Bio</h3>
                <p>{user.bio || "This user hasn't added a bio yet."}</p>
            </div>

            <div>  
                {parseInt(currentUser.id) !== parseInt(userId) && (
                    <button onClick={handleMessageMe}>Message Me</button>
                )}
            </div>
            
            <div>
                {parseInt(currentUser.id) == parseInt(userId) && (
                    <button onClick={handleEditProfile}>Edit Profile</button>
                )}
            </div>
        </div>
        </div>
    );
}

export default UserProfile;
