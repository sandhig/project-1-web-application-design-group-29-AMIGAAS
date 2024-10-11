import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        // Fetch products from Django API
        axios.get('http://127.0.0.1:8000/listings/products/')
            .then(response => {
                setProducts(response.data);  // Store the product data in the state
            });
    }, []);

    return (
        <div>
            <h1>Product List</h1>
            <ul>
                {products.map((product, index) => (
                    <li key={index}>
                        <img src={product.photo_url} alt={product.name} width="50" height="50" />
                        {product.name} - ${product.price}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
