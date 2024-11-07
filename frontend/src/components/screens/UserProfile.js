import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import "./UserProfile.css"
import Header from "../../components/Header"
import { Button, Snackbar } from '@mui/material';
import axios from 'axios';
import { IoSend } from "react-icons/io5";

function UserProfile() {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [products, setProducts] = useState([]);
    const [soldProducts, setSoldProducts] = useState([]);
    const navigate = useNavigate();
    const [message, setMessage] = useState('');
    const [confirmation, setConfirmation] = useState(false);

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
            .then((data) => {
                setUser(data);

                fetch(`http://3.87.240.14:8000/api/user-products/${userId}/`, {
                    method: 'GET',
                    headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => setProducts(data));

                if (userId == currentUser.id) {
                    fetch(`http://3.87.240.14:8000/api/sold-products/`, {
                        method: 'GET',
                        headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.json())
                    .then(data => setSoldProducts(data));
                }
            });
        }

    }, [userId, currentUser, token]);

    useEffect(() => {
        if (user && currentUser) {
          setMessage(`Hi ${user.first_name}, I'm interested in purchasing a product.`);
        }
    }, [user, currentUser]);

    const sendMessageToSeller = () => {
        if (userId) {

            // Fetch or create conversation with seller
            fetch(`http://3.87.240.14:8000/api/conversation/start/${userId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                
                axios.post('http://3.87.240.14:8000/api/send_message/', {
                    conversation_id: data.conversation_id,
                    content: message,
                }, {
                    headers: {
                      'Authorization': `Token ${token}`,
                      'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    console.log('Message sent:', response.data);
                    setConfirmation(true);
                })
                .catch(error => console.error('Error sending message:', error));
 
            });
        }
    };

    const handleCloseConfirmation = () => {
        setConfirmation(false);
    };

    const handleEditProfile = () => {
        navigate(`/profiles/edit-profile`);
    };

    const handleOpenProduct = (id) => {
        navigate(`/products/${id}`);
    };

    return (
        <div>
            <Header />

            {!user ? (<span className="profile-loader"></span>) : (

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
                                <div className="text-input">
                                    <input type="text" value={message} onChange={e => setMessage(e.target.value)}
                                                    onKeyPress={e => {
                                                        if (e.key === 'Enter') {
                                                            sendMessageToSeller()
                                                        }
                                                    }}
                                                />
                                    <button onClick={() => sendMessageToSeller()}><IoSend /></button>
                                </div>
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

                    <span style={{fontWeight:"bold", marginBottom:"10px", marginTop:"30px"}}>Joined</span>
                    <p>{(new Date(user.date_joined)).toLocaleDateString(undefined, { year: 'numeric', month: 'long' })}</p>
                    
                </div>

                <div className="listings-info-container">

                    {parseInt(currentUser.id) == parseInt(userId) ? (
                        <h2 style={{marginTop:"0"}}>My Current Listings</h2>
                    ) : (
                        <h2 style={{marginTop:"0"}}>{user.first_name}'s Listings</h2>
                    )}

                    <div className="profile-products-list">
                        {products.map(product => (
                            <div key={product.id} className="profile-product-item" onClick={() => handleOpenProduct(product.id)}>
                                    {product.image_url ? 
                                    (<img className="profile-product-image" src={product.image_url}></img>) 
                                    : <img className="profile-product-image" src="/images/no-image-icon.png"></img>}
                                    
                                    <div className="product-text">
                                        <div className="product-price">${product.price}</div>
                                        <div className="product-title">{product.name}</div>
                                        <div className="product-location">{product.pickup_location}</div>
                                    </div>
                            </div>
                        ))}
                    </div>

                    {parseInt(currentUser.id) == parseInt(userId) && (
                        <h2>Past Listings</h2>
                    )}

                    <div className="profile-products-list">
                        {soldProducts.map(product => (
                            <div key={product.id} className="profile-product-item" onClick={() => handleOpenProduct(product.id)}>
                                    {product.image_url ? 
                                    (<img className="profile-product-image" src={product.image_url}></img>) 
                                    : <img className="profile-product-image" src="/images/no-image-icon.png"></img>}
                                    
                                    <div className="product-text">
                                        <div className="product-price">${product.price}</div>
                                        <div className="product-title">{product.name}</div>
                                        <div className="product-location">{product.pickup_location}</div>
                                    </div>
                            </div>
                        ))}
                    </div>

                </div>

            </div>
            )}

<Snackbar
                    open={confirmation}
                    autoHideDuration={3000}
                    onClose={handleCloseConfirmation}
                    message="Message sent successfully!"
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                />
                    
        </div>
    );
}

export default UserProfile;
