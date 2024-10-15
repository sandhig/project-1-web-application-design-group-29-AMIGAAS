import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import './PrivateMessage.css';

function PrivateMessage({ currentUserId }) {
    const [conversations, setConversations] = useState([]);
    const [selectedConversationId, setSelectedConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const ws = useRef(null);
    const isUnmounting = useRef(false);
    const location = useLocation();

    const fetchConversations = () => {
        fetch(`http://localhost:8000/api/conversations/`)
            .then(response => response.json())
            .then(data => {
                setConversations(data.conversations);
            });
    };

    useEffect(() => {
        
        fetchConversations();

        // Check if a user is selected
        const searchParams = new URLSearchParams(location.search);
        const userId = searchParams.get('userId');

        // Fetch or create conversation with user
        if (userId) {
            fetch(`http://localhost:8000/api/conversation/start/${userId}/`, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                setSelectedConversationId(data.conversation_id);
                fetchConversations();
            });
        }
    }, [location.search]);

    useEffect(() => {
        if (selectedConversationId) {
            // Fetch messages for the selected conversation
            fetch(`http://localhost:8000/api/conversation/${selectedConversationId}/messages/`)
                .then(response => response.json())
                .then(data => {
                    setMessages(data.messages);
                });

            ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${selectedConversationId}/`);

            ws.current.onmessage = function (e) {
                const data = JSON.parse(e.data);
                const message = data.message;

                setMessages(prevMessages => {
                    if (prevMessages.some(m => m.id === message.id)) {
                        return prevMessages;
                    }
                    return [...prevMessages, message];
                });

            };

            ws.current.onclose = function (e) {
                if (!isUnmounting.current) {
                    console.error('Chat socket closed unexpectedly');
                } else {
                    console.log('Chat socket closed due to component unmounting');
                }
            };

            return () => {
                isUnmounting.current = true;
                if (ws.current) {
                    ws.current.close();
                }
            };
        }
    }, [selectedConversationId]);

    const sendMessage = () => {
        if (input !== '') {
            ws.current.send(
                JSON.stringify({
                    content: input,
                    sender_id: currentUserId
                })
            );
            setInput('');

            fetchConversations();
        }
    };

    const selectedConversation = conversations.find(c => c.id === selectedConversationId);

    return (
        <div className="private-message-container">
            <div className="conversations-list">
                <h2>Conversations</h2>
                <ul>
                    {conversations.map(conversation => (
                    <li
                        key={conversation.id}
                        onClick={() => setSelectedConversationId(conversation.id)}
                        className={
                        conversation.id === selectedConversationId ? 'selected' : ''
                        }
                    >
                        {conversation.name}
                    </li>
                    ))}
                </ul>
                </div>
                <div className="messages-area">
                {selectedConversationId ? (
                    <div>
                    <h2>
                        Conversation with{' '}
                        {selectedConversation ? selectedConversation.name : ''}
                    </h2>
                    <div className="message-list">
                        {messages.map(message => (
                        <div key={message.id} className="message">
                            <strong>{message.sender_name}:</strong> {message.content}
                        </div>
                        ))}
                    </div>
                    <input
                        type="text"
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyPress={e => {
                        if (e.key === 'Enter') {
                            sendMessage();
                        }
                        }}
                    />
                    <button onClick={sendMessage}>Send</button>
                    </div>
                ) : (
                    <div>Select a conversation</div>
                )}
            </div>
      </div>
    );
}

export default PrivateMessage;
