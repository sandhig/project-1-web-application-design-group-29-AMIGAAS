import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {Link} from 'react-router-dom'; 
import IconButton from "@mui/material/IconButton";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import './ProductListing.css';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useUser } from '../../context/UserContext';
import { TextField, Button, Snackbar } from '@mui/material';
import { IoSend } from "react-icons/io5";
import Header from "../../components/Header"

const ProductListing = () => {

    const { id } = useParams();
    const [product, setProduct] = useState([]);
    const token = localStorage.getItem('authToken');
    const { currentUser } = useUser();
    const [confirmation, setConfirmation] = useState(false);
    
    const navigate = useNavigate();
    const [isFavorited, setIsFavorited] = useState(false);
    const [message, setMessage] = useState('');

    const timestamp = new Date(product.created_at);
    const currentDate = new Date();
    const days = Math.floor((currentDate - timestamp) / (1000 * 60 * 60 * 24));
    
    useEffect(() => {
        fetch(`http://3.87.240.14:8000/api/products/${id}`, {
            headers: {
            'Authorization': `Token ${token}`,
            }
        })
        .then(response => response.json())
        .then(data => setProduct(data))
        .catch(error => console.error('Error fetching products:', error));
    }, [id]);
    
    const handleToggleFavorite = () => {
        setIsFavorited(prev => !prev);
    };

    const handleBack = () => {
        navigate(-1); // This navigates back to the previous page
    };

    const sendMessageToSeller = () => {
        if (product.user) {

            // Fetch or create conversation with seller
            fetch(`http://3.87.240.14:8000/api/conversation/start/${product.user.id}/`, {
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
    }

    const handleCloseConfirmation = () => {
        setConfirmation(false);
    };

    useEffect(() => {
        if (product.user && currentUser) {
          setMessage(`Hi ${product.user.first_name}, my name is ${currentUser.first_name} and I'm interested in purchasing ${product.name}. Is it still available?`);
        }
    }, [product, currentUser]);
    
    return (
        <div className="listing-page-container">

            <Header />
            
            <div style={{ width: "fit-content" }} onClick={handleBack}>
                <IconButton type="submit" aria-label="back" className="back-to-listings">
                    <ArrowBackIcon style={{ fill: "grey", fontSize: "medium" }} />
                    <div>Back</div>
                </IconButton>
            </div>
            
            {product ? (
                <div className="listing-container">
                    <img className="listing-image" src={product.image_url}></img>
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
                        <button onClick={() => sendMessageToSeller()}><IoSend /></button>
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

        </div>
    )
} 

export default ProductListing;