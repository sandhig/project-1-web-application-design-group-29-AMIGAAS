import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {Link} from 'react-router-dom'; 
import IconButton from "@mui/material/IconButton";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import './ProductListing.css';
import { useParams } from 'react-router-dom';

const ProductListing = () => {
    console.log('ProductListing component rendered');
    const { id } = useParams();
    const [product, setProduct] = useState([]);
    const token = localStorage.getItem('authToken');
    
    const navigate = useNavigate();
    const [isFavorited, setIsFavorited] = useState(false);

    const timestamp = new Date(product.created_at);
    const currentDate = new Date();
    const days = Math.floor((currentDate - timestamp) / (1000 * 60 * 60 * 24));
    
    useEffect(() => {
        console.log('useEffect triggered');
        console.log('id:', id)
        fetch(`http://3.87.240.14:8000/api/products/${id}`, {
            headers: {
            'Authorization': `Token ${token}`,
            }
        })
        .then(response => response.json())
        .then(data => setProduct(data))
        .catch(error => console.error('Error fetching products:', error));
    }, [id]);
    
    console.log(product);
    
    const handleToggleFavorite = () => {
        setIsFavorited(prev => !prev);
    };

    const handleBack = () => {
        navigate(-1); // This navigates back to the previous page
    };
    
    return (
        <div className="listing-page-container">
            
            <div style={{ width: "fit-content" }} onClick={handleBack}>
                <IconButton type="submit" aria-label="back" className="back-to-listings">
                    <ArrowBackIcon style={{ fill: "grey", fontSize: "medium" }} />
                    <div>Back to listings</div>
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
                        <div>{product.user.first_name} {product.user.last_name} ({product.user.email})</div>)
                        : (<p>Loading user info...</p>)}
                    </span>
                </div>
            ) : (
                <p>No product info</p>
            )}
            

        </div>
    )
} 

export default ProductListing;