//basic structure for this page, including some placeholder content for tabs like FAQ, About and Dark Mode
import React from 'react';

function HelpAndSettings() {
    return (
        <div style={{ padding: '20px' }}>
            <h1>Help & Settings</h1>
            <div>
                <h2>FAQ</h2>
                <p>Here you'll find answers to frequently asked questions.</p>
            </div>
            <div>
                <h2>About</h2>
                <p>Too Good To Throw is a platform created to help students exchange items easily.</p>
            </div>
            <div>
                <h2>Dark Mode</h2>
                <p>Switch between light and dark themes for a better viewing experience.</p>
            </div>
        </div>
    );
}

export default HelpAndSettings;
