/* About.js good3*/

import React, { useState } from 'react';
import Header from "../../components/Header";
import './About.css';

const teamMembers = [
    { id: 1, name: 'Tasfia', fullName: 'Tasfia Mehbuba Islam', role: 'Computer Engineering', image: 'https://www.shutterstock.com/image-vector/cute-cartoon-girl-bow-lollipop-600nw-2193282125.jpg', bio: 'Frontend developer specializing in database management.',
        linkedin: 'https://www.linkedin.com/in/tasfia-mehbuba-islam/',
        github: 'https://github.com/tasfia8' 
     },
    { id: 2, name: 'Amy', fullName: 'Amy Saranchuk', role: 'Engineering Science', image: 'https://images.aiscribbles.com/fde2f799da4e4ab585c586f37149a822.png?v=908b7e', bio: 'Software developer focusing on creating intuitive and beautiful user interfaces.',
        linkedin: 'https://www.linkedin.com/in/amysaranchuk/',
        github: 'https://github.com/amyy2/'
     },
    { id: 3, name: 'Lamia', fullName: 'Lamia Alam', role: 'Computer Engineering', image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHjcqA8gmqYRP2guO27QRSxl6iRoFTgJpeFQ&s', bio: 'Software developer specializing in product quality',
        linkedin: 'https://www.linkedin.com/in/lamia-alam-29a53a1a0/',
        github: 'https://github.com/lamia-alam/'
     },
    { id: 4, name: 'Raisa', fullName: 'Raisa Islam Aishy', role: 'Computer Engineering', image: 'https://static.vecteezy.com/system/resources/previews/008/974/656/non_2x/cute-kid-girl-holding-bubble-milk-tea-hand-drawn-cartoon-character-illustration-vector.jpg', bio: 'Software developer focusing on Unit Testing and UI/UX',
        linkedin: 'https://www.linkedin.com/in/raisa-islam-aishy/',
        github: 'https://github.com/ria147/'
     },
    { id: 5, name: 'Sarah', fullName: 'Sarah Agib', role: 'Engineering Science', image: 'https://static.vecteezy.com/system/resources/thumbnails/020/767/287/small_2x/cute-girl-holding-a-cat-kid-with-animal-character-cartoon-hand-draw-art-illustration-vector.jpg', bio: 'Software developer focusing on product quality and bug testing.',
        linkedin: 'https://www.linkedin.com/in/sarah-agib/',
        github: 'https://github.com/sarahagib/'
     },
    { id: 6, name: 'Bavya', fullName: 'Bavya Mittal', role: 'Computer Engineering', image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo9zMmNF-qUMMWxgjFLLsmzA7wiuO3xwi3vw&s', bio: 'Software developer focusing on User Interface',
        linkedin: 'https://www.linkedin.com/in/bavya-mittal/',
        github: 'https://github.com/BavyaMittal'
     },
    { id: 7, name: 'Sandhi', fullName: 'Sandhi Ganjoo', role: 'Engineering Science', image: 'https://img.freepik.com/premium-vector/cute-girl-cartoon-hug-sweet-heart-valentines-day-kawaii-character_70350-730.jpg', bio: 'Software developer focusing on User Interface',
        linkedin: 'https://www.linkedin.com/in/sandhiganjoo/',
        github: 'https://github.com/sandhig'
     },
];


function About() {
    const [selectedMember, setSelectedMember] = useState(null);
    const [isFlipped, setIsFlipped] = useState(false); // Manage flip with this state

    const handleMemberClick = (member) => {
        setSelectedMember(member);
    };

    const closePopup = () => {
        setSelectedMember(null);
    };

    const handleNavigation = (direction) => {
        const currentIndex = teamMembers.findIndex(member => member === selectedMember);
        const nextIndex = (currentIndex + direction + teamMembers.length) % teamMembers.length;
        setSelectedMember(teamMembers[nextIndex]);
    };

    //Flip state Toggler
    const toggleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    return (
        <div className="about-page">
            <Header />
            <div className="about-content">
                <h1>About Us</h1>
                
                <div className="circle-container">
                    <div className={`center-circle ${isFlipped ? 'flipped' : ''}`} onClick={toggleFlip}>
                        <div className="front">AMIGAAS</div>
                        <div className="back">
                            <p>A: Aishy</p>
                            <p>M: Mittal</p>
                            <p style={{ marginLeft: '4px' }}>I: Islam</p> {/* Inline style for adjustment */}
                            <p>G: Ganjoo</p>
                            <p>A: Alam</p>
                            <p>A: Agib</p>
                            <p>S: Saranchuk</p>
                        </div>
                    </div>
                    {teamMembers.map((member, index) => (
                        <div
                            key={member.id}
                            className="team-member-circle"
                            onClick={() => handleMemberClick(member)}
                            style={{
                                transform: `rotate(${index * (360 / teamMembers.length)}deg) translate(0px, -200px) rotate(-${index * (360 / teamMembers.length)}deg)`,
                            }}
                        >
                            <img src={member.image} alt={member.name} />
                            <div className="team-member-name">{member.name}</div>
                        </div>
                    ))}
                </div>
                {selectedMember && (
                    <div className="popup">
                        <button className="close-btn" onClick={closePopup}>X</button>
                        <img src={selectedMember.image} alt={selectedMember.fullName} className="popup-img" />
                        <h2>{selectedMember.fullName}</h2>
                        <h3>{selectedMember.role}</h3>
                        <p>{selectedMember.bio}</p>

                        {/* Social Links */}
                        <div className="social-links">
                            <a href={selectedMember.linkedin} target="_blank" rel="noopener noreferrer" className="social-link">
                                <i className="fab fa-linkedin"></i>
                            </a>
                            <a href={selectedMember.github} target="_blank" rel="noopener noreferrer" className="social-link">
                                <i className="fab fa-github"></i>
                            </a>
                        </div>

                        <div className="navigation-buttons">
                            <button onClick={() => handleNavigation(-1)}>&larr;</button>
                            <button onClick={() => handleNavigation(1)}>&rarr;</button>
                        </div>
                    </div>
                )}
            </div>
            <div className="description-section">
                <h2>Too Good To Throw</h2>
                <p>We are AMIGAAS, a team of 7 University of Toronto Engineering students who developed "Too Good to Throw" to promote affordable, sustainable shopping for students.</p>
            </div>
        </div>
    );
}

export default About;