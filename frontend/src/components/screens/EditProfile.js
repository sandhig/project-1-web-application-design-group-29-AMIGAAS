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

    const { currentUser } = useUser();
    const token = localStorage.getItem('authToken');
    const [formErrors, setFormErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState('');
    const [selectedImage, setSelectedImage] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const isFormInvalid = isSubmitting || Object.values(formErrors).some(error => error);

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
                setSelectedImage(data.profilePic);
            })
            .catch(error => console.error('Error fetching profile:', error));
        }
    }, [currentUser, token]);

    const validateImageType = (file) => {
        if (file && !file.type.includes('jpeg') && !file.name.endsWith('.jpg')) {
            return 'Please upload a .jpg or .jpeg file';
        } else {
            return '';
        }
    };

    const handleInputChange = (event) => {
        const { name, value, type, files } = event.target;
        setFormErrors({ ...formErrors, [name]: '' });

        if (type === 'file') {
            const file = files[0];

            if (!file) {
                return;
            }

            // Check if the file type is JPEG
            const wrongFileType = validateImageType(file);
            if (wrongFileType) {
                setFormErrors({
                    ...formErrors,
                    image: wrongFileType
                });
    
                // Reset the profile pic to null if there's an error
                setProfile({
                    ...profile,
                    profilePic: null
                });
                return;
            }

            setFormErrors({...formErrors, image: ''});
            setProfile({ ...profile, image: file });
            setSelectedImage(URL.createObjectURL(file));

        } else {
            setProfile({
                ...profile,
                [name]: value
                });
        }
    };

    const handleSave = (e) => {
        e.preventDefault();

        const errors = {
            image: validateImageType(profile.profilePic),
        };
      
        const hasErrors = Object.values(errors).some(error => error !== '');
        if (hasErrors) {
            setFormErrors(errors);
            return;
        }
      
        setIsSubmitting(true);

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
        .catch(error => console.error('Error:', error))
        .finally(() => setIsSubmitting(false));
    };

    return (
        <div >
            <Header />
            <div className="edit-profile-container">
                <h1>Edit Profile</h1>
                <form noValidate onSubmit={handleSave} className='profile-form'>
                    <div className="profile-photo-container">
                        {selectedImage ? (
                            <img className="profile-photo" src={selectedImage} alt="Profile Photo"></img>
                        ) : (
                            <img src="/profile-icon.jpg" alt="Default Profile" className="profile-photo" />
                        )}
                        <input 
                            id="imageInput"
                            type="file" 
                            accept="image/jpg, image/jpeg"  
                            onChange={handleInputChange} 
                            style={{ display: 'none' }}
                        />
                        <label htmlFor="imageInput">
                            <Button
                                variant="contained"
                                color="primary"
                                component="span"
                                disabled={isSubmitting}
                                sx={{
                                    '&:hover': {
                                    backgroundColor: '#007fa3',       // Custom hover color
                                    },
                                }}
                            >
                                Choose Image
                            </Button>
                        </label>
                        <Typography variant="caption" color="error">{formErrors.image}</Typography>
                    </div>
                    <TextField
                        label="First Name"
                        name="first_name"
                        type="text"
                        value={profile.first_name}
                        variant="outlined"
                        disabled
                        sx={{ input: { cursor: 'not-allowed' } }}
                    />
                    <TextField
                        label="Last Name"
                        name="last_name"
                        type="text"
                        value={profile.last_name}
                        variant="outlined"
                        disabled
                        sx={{ input: { cursor: 'not-allowed' } }}
                    />
                    <TextField
                        label="Bio"
                        name="bio"
                        value={profile.bio}
                        onChange={handleInputChange}
                        multiline
                        rows={4}
                        variant="outlined"
                    />
                    <Button
                        name="submit"
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
                        {isSubmitting ? 'Saving Changes...' : 'Save Changes'}
                    </Button>
                    {successMessage && <p className="success-message">{successMessage}</p>}
                </form>
            </div>
        </div>
    );
}

export default EditProfile;
