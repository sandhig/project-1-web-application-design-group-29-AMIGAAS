import React from 'react';
import Header from "../../components/Header"

function About() {
    return (
        <div>
            <Header/>
            <div style={{ padding: '20px' }}>
                <h1>About Us</h1>
                <p>We are AMIGAAS, a team of 7 University of Toronto Engineering students who developed "Too Good to Throw" as a platform to help students buy and sell second-hand items affordably and sustainably.</p>
                {/* Placeholder for adding team members' photos and names in the future */}
            </div>
        </div>
    );
}

export default About;
