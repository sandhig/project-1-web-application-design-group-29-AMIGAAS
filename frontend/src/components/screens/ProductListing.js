import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import {Link} from 'react-router-dom'; 
import IconButton from "@mui/material/IconButton";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import './ProductListing.css';

const ProductListing = () => {
    const location = useLocation()
    const { product } = location.state

    const timestamp = new Date(product.created_at);
    const currentDate = new Date();
    const days = Math.floor((currentDate - timestamp) / (1000 * 60 * 60 * 24));

    const [isFavorited, setIsFavorited] = useState(false);

    const handleToggleFavorite = () => {
        setIsFavorited(prev => !prev);
    };

    console.log(product)

    return (
        <div className="listing-page-container">
            <Link to="/products">
                <IconButton type="submit" aria-label="back" className="back-to-listings">
                    <ArrowBackIcon style={{ fill: "grey", fontSize: "medium" }} />
                    <div>Back to listings</div>
                </IconButton>
            </Link>

            {product ? (
                <div className="listing-container">
                    <img className="listing-image" src={product.image_url}></img>
                    <span className="listing-details">
                        <div className="listing-header">
                            <div className="listing-title">{product.name}</div>
                            <IconButton aria-label="favourite" onClick={handleToggleFavorite}>
                                {isFavorited ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                            </IconButton>
                        </div>
                        <hr></hr>
                        <div className="listing-price">${product.price}</div>
                        {days === 0 ? (<p>Listed today</p>) : <p>Listed {days} days ago</p>}
                        <hr></hr>
                        <h2>Product details</h2>
                        <div className="listing-description">{product.description}</div>
                        <div className="listing-categories">
                            <div className="listing-category">{product.category}</div>
                            <div><span style={{ fontWeight: "bold" }}>Condition:</span> {product.condition}</div>
                            <div><span style={{ fontWeight: "bold" }}>Pickup location:</span> {product.pickup_location}</div>
                        </div>
                        <hr></hr>
                        <h2>Seller information</h2>
                        <div>{product.user.first_name} {product.user.last_name}</div>
                        <div>{product.user.email}</div>
                    </span>
                </div>
            ) : (
                <p>No product info</p>
            )}

        </div>
    )
} 

export default ProductListing;