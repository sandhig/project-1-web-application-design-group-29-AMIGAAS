import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom'; 
import IconButton from "@mui/material/IconButton";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import './ProductListing.css';
import axios from 'axios';
import { Snackbar, TextField } from '@mui/material';
import { IoSend } from "react-icons/io5";

const ProductView = ({
        product, 
        currentUser
    }) => {

    const token = localStorage.getItem('authToken');
    const [confirmation, setConfirmation] = useState(false);
    const [isFavorited, setIsFavorited] = useState(false);
    const [message, setMessage] = useState('');
    const [isMessageButtonDisabled, setIsMessageButtonDisabled] = useState(false);

    const timestamp = new Date(product.created_at);
    const currentDate = new Date();
    const days = Math.floor((currentDate - timestamp) / (1000 * 60 * 60 * 24));

    useEffect(() => {
        fetch(`http://54.165.176.36:8000/api/wishlist/${product.id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => setIsFavorited(data));
    }, [product, currentUser, token]);
    
    const handleToggleFavorite = () => {

        if (isFavorited) {
            // Remove from wishlist
            fetch(`http://54.165.176.36:8000/api/wishlist/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product_id: product.id })
            })
            .then(response => {
                if (response.ok) {
                    setIsFavorited(prev => !prev);
                } else {
                    return response.json().then(data => {
                        console.error('Failed to remove product from wishlist:', data);
                    });
                }
            })
            .catch(error => console.error('Error removing from wishlist:', error))
        } else {
            // Add to wishlist
            fetch(`http://54.165.176.36:8000/api/wishlist/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: product.id })
            })
            .then(response => response.json())
            .then(setIsFavorited(prev => !prev));
        }
    };

    const sendMessageToSeller = () => {
        setIsMessageButtonDisabled(true);
        if (product.user) {

            // Fetch or create conversation with seller
            fetch(`http://54.165.176.36:8000/api/conversation/start/${product.user.id}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                axios.post('http://54.165.176.36:8000/api/send_message/', {
                    conversation_id: data.conversation_id,
                    content: message,
                }, {
                    headers: {
                      'Authorization': `Token ${token}`,
                      'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    setConfirmation(true);
                })
                .catch(error => console.error('Error sending message:', error));
 
            });
        }
    };

    const handleCloseConfirmation = () => {
        setConfirmation(false);
    };

    useEffect(() => {
        if (product.user && currentUser) {
          setMessage(`Hi ${product.user.first_name}, my name is ${currentUser.first_name} and I'm interested in purchasing ${product.name}. Is it still available?`);
        }
    }, [product, currentUser]);
    
    return (
        <>    
        {product ? (
            <div className="listing-container">
                <div className="listing-image-container">
                    {product.image_url ? 
                          (<img className="listing-image" src={product.image_url}></img>) 
                          : <img className="listing-image" src="/images/no-image-icon.png"></img>}
                </div>
                <span className="listing-details">
                    <div className="listing-header">
                        <div className="listing-title">{product.name}</div>
                        
                        <IconButton aria-label="favourite" onClick={handleToggleFavorite} style={{height: "fit-content", width: "fit-content" }}>
                            {isFavorited ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                        </IconButton>
                        
                    </div>
                    
                    <hr></hr>
                    <div className="listing-price">${product.price}</div>
                    
                    {days === 0 ? (<p>Listed today</p>) : <p>Listed {days} days ago</p>}
                    <hr></hr>
                    
                    <h2 style={{margin: "0"}}>Product details</h2>
                    <div className="listing-description">{product.description}</div>
                    
                    <div className="listing-categories">
                        <div className="listing-category">{product.category}</div>
                        <div><span style={{ fontWeight: "bold" }}>Condition:</span> {product.condition}</div>
                        <div><span style={{ fontWeight: "bold" }}>Pickup location:</span> {product.pickup_location}</div>
                    </div>
                    
                    <hr></hr>
                    <h2 style={{margin: "0"}}>Seller information</h2>
                    {product.user ? (
                        <Link to={`/user/${product.user.id}`} className="seller-info" >
                        {product.user.profile_pic ? (
                            <img src={product.user.profile_pic} alt="Profile" className="header-profile"/>
                            ) : (
                            <img src="/profile-icon.jpg" alt="Default Profile" className="header-profile" />
                        )}
                        {product.user.first_name} {product.user.last_name} ({product.user.email})
                        </Link>)
                    : (<p>Loading user info...</p>)}
                    <div className="text-input">
                        <input type="text" value={message} onChange={e => setMessage(e.target.value)}
                                        onKeyPress={e => {
                                            if (e.key === 'Enter') {
                                                sendMessageToSeller()
                                            }
                                        }}
                                    />
                        <button onClick={() => sendMessageToSeller()} disabled={isMessageButtonDisabled}><IoSend /></button>
                    </div>
                </span>
                <Snackbar
                    open={confirmation}
                    autoHideDuration={3000}
                    onClose={handleCloseConfirmation}
                    message="Message sent successfully!"
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                />
            </div>
        
        ) : (
            <p>No product info</p>
        )}
        </>
        
    )
} 

export default ProductView;