import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';

function UserProfile() {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const { currentUser } = useUser();

    const token = localStorage.getItem('authToken');

    useEffect(() => {
        if (currentUser) {
            fetch(`http://3.87.240.14:8000/api/profile/${userId}/`, {
                method: 'GET',
                headers: {
                  'Authorization': `Token ${token}`,
                  'Content-Type': 'application/json',
                },
              })
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
            <h1>{user.first_name}</h1>
            {parseInt(currentUser.id) !== parseInt(user.id) && (
                <button onClick={handleMessageMe}>Message Me</button>
            )}
        </div>
    );
}

export default UserProfile;
