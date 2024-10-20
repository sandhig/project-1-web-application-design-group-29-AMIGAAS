import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

function UserProfile() {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const { currentUser } = useUser();

    useEffect(() => {
        if (currentUser) {
            fetch(`http://localhost:8000/api/profile/${userId}/`)
                .then(response => response.json())
                .then(data => setUser(data));
        }
    }, [userId]);

    const handleMessageMe = () => {
        navigate(`/messages?userId=${userId}`);
    };

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{user.name}</h1>
            {parseInt(currentUser.id) !== parseInt(user.id) && (
                <button onClick={handleMessageMe}>Message Me</button>
            )}
        </div>
    );
}

export default UserProfile;
