/* About.js */

import React, { useState } from 'react';
import Header from "../../components/Header";
import './About.css';

const teamMembers = [
    { id: 1, name: 'Tasfia', fullName: 'Tasfia Mehbuba Islam', role: 'Computer Engineering', 
        image: '/images/team/tasfia.png', bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/tasfia-mehbuba-islam/',
        github: 'https://github.com/tasfia8' 
     },
    { id: 2, name: 'Amy', fullName: 'Amy Saranchuk', role: 'Engineering Science', image: '/images/team/amy.jpg', 
        bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/amysaranchuk/',
        github: 'https://github.com/amyy2/'
     },
    { id: 3, name: 'Lamia', fullName: 'Lamia Alam', role: 'Computer Engineering', 
        image: '/images/team/lamia3.jpg', bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/lamia-alam-29a53a1a0/',
        github: 'https://github.com/lamia-alam/'
     },
    { id: 4, name: 'Raisa', fullName: 'Raisa Islam Aishy', role: 'Computer Engineering', 
        image: '/images/team/raisa.jpeg', bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/raisa-islam-aishy/',
        github: 'https://github.com/ria147/'
     },
    { id: 5, name: 'Sarah', fullName: 'Sarah Agib', role: 'Engineering Science', 
        image: '/images/team/sarah.jpeg', bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/sarah-agib/',
        github: 'https://github.com/sarahagib/'
     },
    { id: 6, name: 'Bavya', fullName: 'Bavya Mittal', role: 'Computer Engineering', 
        image: '/images/team/bavya.png', bio: 'Frontend & Backend Developer',
        linkedin: 'https://www.linkedin.com/in/bavya-mittal/',
        github: 'https://github.com/BavyaMittal'
     },
    { id: 7, name: 'Sandhi', fullName: 'Sandhi Ganjoo', role: 'Engineering Science', 
        image: '/images/team/sandhi.png', bio: 'Frontend & Backend Developer',
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
                <h1>Our Team</h1>
                
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
                <p>We are AMIGAAS, a team of 4th year University of Toronto Engineering students 
                    who developed "Too Good to Throw" to promote affordable, sustainable shopping for students. Too Good to Throw is a centralized marketplace to make buying and
                    selling secondhand items simple, safe, and sustainable. This platform, exclusive to the U of T community, 
                    allows members to buy/sell textbooks, furniture, household items, and more. Accounts are verified by only allowing university-approved emails and  
                    users can choose campus-based pickup locations, create new listings, engage in private messaging, and have personalized wishlists.</p>
            </div>
        </div>
    );
}

export default About;