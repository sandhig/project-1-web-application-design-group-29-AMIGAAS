import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import './EditProfile.css';
import Header from "../../components/Header"

function EditProfile() {
    
    const navigate = useNavigate();

    const [profile, setProfile] = useState({
        first_name: '',
        last_name: '',
        bio: '',
        profilePic: null
    });

    const [profilePicPreview, setProfilePicPreview] = useState(null);
    const { currentUser } = useUser();
    const token = localStorage.getItem('authToken');

    const [successMessage, setSuccessMessage] = useState('');

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
                    profilePic: data.profilePic || ''
                });
                setProfilePicPreview(data.profilePic)
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

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setProfile(prevProfile => ({
            ...prevProfile,
            profilePic: file,
        }));
        setProfilePicPreview(URL.createObjectURL(file));  // Preview the selected image
    };

    const handleSave = (e) => {
        e.preventDefault();

        // Structure data to match what the serializer expects
        const formData = new FormData();
        formData.append('first_name', profile.first_name);
        formData.append('last_name', profile.last_name); 
        formData.append('bio', profile.bio); 
        
        // Only add profile pic to form if it's a new file
        if (profile.profilePic && typeof profile.profilePic !== 'string') {
            formData.append('profilePic', profile.profilePic);
        }
    
        /*const updatedProfile = {
            user: {
                first_name: profile.first_name,
                last_name: profile.last_name,
            },
            bio: profile.bio,
            profilePic: profile.profilePic,
        };*/

        fetch(`http://3.87.240.14:8000/api/profiles/edit-profile/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
            },
            body: formData //JSON.stringify(updatedProfile),
        })
        .then(response => {
            if (response.ok) {
                setSuccessMessage('Profile saved successfully!'); // Set success message
                setTimeout(() => setSuccessMessage(''), 3000); // Clear message after 3 seconds
                navigate(`/user/${currentUser.id}`);
            } else {
                console.error('Error saving profile:', response);
            }
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div className="edit-profile-container">
            <Header />
            <h1>Edit Profile</h1>
            <form onSubmit={handleSave} className='profile-form'>
                <label className="profile-label">
                    First Name:
                    <input
                        type="text"
                        name="first_name"
                        value={profile.first_name}
                        onChange={handleChange}
                        className="profile-input"
                    />
                </label>
                <label className="profile-label">
                    Last Name:
                    <input
                        type="text"
                        name="last_name"
                        value={profile.last_name}
                        onChange={handleChange}
                        className="profile-input"
                    />
                </label>
                <label className='profile-label'>
                    Bio:
                    <textarea
                        name="bio"
                        value={profile.bio}
                        onChange={handleChange}
                        className='profile-textarea'
                        row="5"
                    />
                </label>
                <label>
                    Profile Photo:
                    <input
                        type="file"
                        onChange={handleFileChange}  // Update file input handler
                        className="profile-photo-input"
                        accept="image/*"
                    />
                </label>

                {profilePicPreview && (
                    <img src={profilePicPreview} 
                    alt="Profile Preview" 
                    style={{ width: '100px', height: '100px', borderRadius: '50%' }} 
                    />
                )}
                <button type="submit" className="profile-save-button">Save Changes</button>
                {successMessage && <p className="success-message">{successMessage}</p>}
            </form>
        </div>
    );
}

export default EditProfile;
