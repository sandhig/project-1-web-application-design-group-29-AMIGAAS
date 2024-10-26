import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';

function EditProfile() {
    const [profile, setProfile] = useState({
        first_name: '',
        last_name: '',
        bio: '',
    });
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();
    const { currentUser } = useUser();
    const token = localStorage.getItem('authToken');

    useEffect(() => {
        // Fetch profile data to populate form fields
        if (currentUser) {
            fetch(`http://3.87.240.14:8000/api/user/${currentUser.id}/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                setProfile({
                    first_name: data.first_name || '',
                    last_name: data.last_name || '',
                    bio: data.bio || '',
                });
            })
            .catch(error => console.error('Error fetching profile:', error));
        }
    }, [currentUser, token]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile(prevProfile => ({
            ...prevProfile,
            [name]: value,
        }));
    };

    const handleSave = (e) => {
        e.preventDefault();

        fetch(`http://3.87.240.14:8000/api/profiles/edit-profile/`, {
            method: 'PUT',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profile),
        })
        .then(response => {
            if (response.ok) {
                setSuccessMessage('Profile saved successfully!'); // Set success message
                setTimeout(() => setSuccessMessage(''), 3000); // Clear message after 3 seconds
                navigate(`/profile/${currentUser.id}`);
            } else {
                console.error('Error saving profile:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div className="edit-profile-container">
            <h1>Edit Profile</h1>
            <form onSubmit={handleSave}>
                <label>
                    First Name:
                    <input
                        type="text"
                        name="first_name"
                        value={profile.first_name}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Last Name:
                    <input
                        type="text"
                        name="last_name"
                        value={profile.last_name}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Bio:
                    <textarea
                        name="bio"
                        value={profile.bio}
                        onChange={handleChange}
                    />
                </label>
                <button type="submit">Save Changes</button>
            </form>
        </div>
    );
}

export default EditProfile;
