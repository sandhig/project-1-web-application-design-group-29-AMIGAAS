import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import IconButton from "@mui/material/IconButton";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import './ProductListing.css';
import { useParams } from 'react-router-dom';
import { useUser } from '../../../context/UserContext';
import Header from "../../Header";
import ProductView from "./ProductView";
import ProductEdit from './ProductEdit';

const ProductListing = () => {

    const { id } = useParams();
    const [product, setProduct] = useState([]);
    const token = localStorage.getItem('authToken');
    const { currentUser } = useUser();
    const navigate = useNavigate();
    const [editable, setEditable] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isNull, setIsNull] = useState(false);

    useEffect(() => {
        fetch(`http://54.165.176.36:8000/api/products/${id}`, {
            headers: {
                'Authorization': `Token ${token}`,
            }
        })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        console.error("Listing not found");
                        setIsNull(true);
                        setLoading(false)
                        return null;
                    } else {
                    throw new Error(`Error fetching listing: ${response.statusText}`);
                    }
                }
                return response.json()
            })
            .then(data => {
                setProduct(data);
                if (data.user && currentUser) {
                    setEditable(data.user.id === currentUser.id);
                    setLoading(false)
                }
            })
            .catch(error => console.error('Error fetching product:', error));
    }, [id, currentUser, token]);

    const handleBack = () => {
        navigate(-1); // This navigates back to the previous page
    };

    return (

        <div className="listing-page-container">

            <Header />

            <div style={{ width: "fit-content" }} onClick={handleBack}>
                <IconButton type="submit" aria-label="back" className="back-to-listings">
                    <ArrowBackIcon style={{ fill: "grey", fontSize: "medium" }} />
                    <div>Back</div>
                </IconButton>
            </div>

            {loading ? (
                <span className="loader"></span>
            ) : (
                <>
                {isNull ? (
                    <h2>Listing not found</h2>
                ) : (

                <>
                    {editable ? (
                        <>
                            <ProductEdit
                                product={product}
                                currentUser={currentUser}
                            />
                        </>
                    ) : (
                        <ProductView
                            product={product}
                            currentUser={currentUser}
                        />
                    )}
                </>
                )}
                </>
            )}

        </div>

    )
}

export default ProductListing;