/* About.js */

import React, { useState } from 'react';
import Header from "../../components/Header"
import './About.css';

const teamMembers = [
    { id: 1, name: 'Tasfia', fullName: 'Tasfia Mehbuba Islam', role: 'Computer Engineering',
         image: 'https://www.shutterstock.com/image-vector/cute-cartoon-girl-bow-lollipop-600nw-2193282125.jpg', 
         bio: 'Frontend developer specializing in database management.' },
    { id: 2, name: 'Amy', fullName: 'Amy Saranchuk', role: 'Engineering Science', 
        image: 'https://images.aiscribbles.com/fde2f799da4e4ab585c586f37149a822.png?v=908b7e', 
        bio: 'Software developer focusing on creating intuitive and beautiful user interfaces.' },
    { id: 3, name: 'Lamia', fullName: 'Lamia Alam', role: 'Computer Engineering', 
        image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHjcqA8gmqYRP2guO27QRSxl6iRoFTgJpeFQ&s', 
        bio: 'Software developer specializing in product quality' },
    { id: 4, name: 'Raisa', fullName: 'Raisa Islam Aishy', role: 'Computer Engineering', 
        image: 'https://static.vecteezy.com/system/resources/previews/008/974/656/non_2x/cute-kid-girl-holding-bubble-milk-tea-hand-drawn-cartoon-character-illustration-vector.jpg', 
        bio: 'Software developer focusing on Unit Testing and UI/UX' },
    { id: 5, name: 'Sarah', fullName: 'Sarah Agib', role: 'Engineering Science', 
        image: 'https://static.vecteezy.com/system/resources/thumbnails/020/767/287/small_2x/cute-girl-holding-a-cat-kid-with-animal-character-cartoon-hand-draw-art-illustration-vector.jpg', 
        bio: 'Software developer focusing on product quality and bug testing.' },
    { id: 6, name: 'Bavya', fullName: 'Bavya Mittal', role: 'Computer Engineering', 
        image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo9zMmNF-qUMMWxgjFLLsmzA7wiuO3xwi3vw&s', 
        bio: 'Software developer focusing on User Inferface' },
    { id: 7, name: 'Sandhi', fullName: 'Sandhi Ganjoo', role: 'Engineering Science', 
        image: 'https://img.freepik.com/premium-vector/cute-girl-cartoon-hug-sweet-heart-valentines-day-kawaii-character_70350-730.jpg', 
        bio: 'Software developer focusing on User Inferface' },
];

function About() {
    const [selectedMember, setSelectedMember] = useState(null);

    const handleMemberClick = (member) => {
        setSelectedMember(member);
    };

    const closePopup = () => {
        setSelectedMember(null);
    };

    return (
        <div>
            <Header/>
            <div className="about-container">
                <h1>About Us</h1>
                <p>We are AMIGAAS, a team of 7 University of Toronto Engineering students who developed "Too Good to Throw" to promote affordable, sustainable shopping for students.</p>
                
                

                {/* Popup Modal for Member Details */}
                {selectedMember && (
                    <div className="popup-overlay" onClick={closePopup}>
                        <div className="popup-content" onClick={(e) => e.stopPropagation()}>
                            <h2>{selectedMember.fullName}</h2>
                            <img src={selectedMember.image} alt={selectedMember.name} className="popup-image" />
                            <p><strong>Major:</strong> {selectedMember.role}</p>
                            <p>{selectedMember.bio}</p>
                            <div className="popup-buttons">
                                <button onClick={closePopup}>Close</button>
                            </div>
                        </div>
                    </div>
                )}

                {/* Too Good to Throw Description */}
                <div className="about-description">
                    <h2>Too Good to Throw</h2>
                    <p>This platform empowers students to buy and sell second-hand items conveniently within the university community, promoting sustainability and affordability.</p>
                </div>
            </div>
        </div>
    );
}

export default About;