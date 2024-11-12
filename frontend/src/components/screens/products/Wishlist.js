import { useUser } from '../../../context/UserContext';
import React, { useState, useEffect } from 'react';
import Header from "../../Header"
import { useNavigate } from 'react-router-dom';
import './Wishlist.css';
import IconButton from "@mui/material/IconButton";
import ClearIcon from '@mui/icons-material/Clear';

function Wishlist() {

    const token = localStorage.getItem('authToken');
    const { currentUser } = useUser();
    const [wishlistItems, setWishlistItems] = useState([]);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    const fetchWishlistItems = () => {
        fetch('http://54.165.176.36:8000/api/wishlist/', {
            headers: {
                'Authorization': `Token ${token}`,
            }
        })
        .then(response => response.json())
        .then((data) => {
            setWishlistItems(data);
            setLoading(false);
        })
        .catch(error => console.error('Error fetching wishlist:', error));
    };

    useEffect(() => {
        fetchWishlistItems();
    }, [currentUser]);

    const handleOpenProduct = (id) => {
        navigate(`/products/${id}`);
    };

    const handleRemove = (id) => {
        const confirmed = window.confirm("Are you sure you want to remove this item from your wishlist?");

        if (confirmed) {
            fetch(`http://54.165.176.36:8000/api/wishlist/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product_id: id })
            })
            .then(response => {
                if (response.ok) {
                    console.log('Product removed from wishlist');
                    fetchWishlistItems();
                } else {
                    return response.json().then(data => {
                        console.error('Failed to remove product from wishlist:', data);
                    });
                }
            })
            .catch(error => console.error('Error removing from wishlist:', error));
        }
    };
    
    return (
        <div>
            <Header />
            <div style={{ padding: '10px' }}></div>
            <h1 className="wishlist-title">My Wishlist</h1>
            <div className="product-grid-wrapper">
                <div className="product-grid transparent-bg">
                {loading ? (<span className="loader"></span>) : (
                    <>
                    {wishlistItems.length > 0 ? (
                    <div className="products">
                        {wishlistItems.map(item => (
                            <div key={item.id} className="product-item">
                                <div onClick={() => handleOpenProduct(item.id)} style={{position:"relative"}}>

                                    <IconButton 
                                        className="remove-from-wishlist" 
                                        onClick={(event) => {
                                            event.stopPropagation();
                                            handleRemove(item.id);
                                        }}
                                    >
                                        <ClearIcon style={{ fill: "white", fontSize: "medium" }} />
                                    </IconButton>

                                    {item.image_url ? 
                                    (<img className="product-image" src={item.image_url}></img>) 
                                    : <img className="product-image" src="/images/no-image-icon.png"></img>}

                                    
                                    <div className="product-text">
                                        <div className="product-price">${item.price}</div>
                                        <div className="product-title">{item.name}</div>
                                        <div className="product-location">{item.pickup_location}</div>
                                    </div>

                                </div>
                            </div>
                        ))}
                    </div>
                    ) : (
                    <h3>Products you like will appear here</h3>
                    )}</>
                    )}
                </div>
            </div>
        </div>
    
    );
}

export default Wishlist