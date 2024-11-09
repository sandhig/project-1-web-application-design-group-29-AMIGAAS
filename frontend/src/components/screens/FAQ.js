import React from 'react';
import Header from "../../components/Header"

function FAQ() {
    return (
        <div>
            <Header/>
            <div style={{ padding: '20px' }}>
                <h1>Frequently Asked Questions (FAQ)</h1>
                <h2>Shopping on Too Good To Throw</h2>
                <p>Q: How do I buy items on this platform?</p>
                <p>A: Simply browse listings and contact the seller for further details.</p>
                {/* Add more FAQs related to sign-up, login, purchasing, etc. */}
            </div>
        </div>
    );
}

export default FAQ;
