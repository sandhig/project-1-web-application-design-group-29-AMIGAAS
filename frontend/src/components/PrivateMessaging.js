import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import './PrivateMessage.css';
import { IoSend } from "react-icons/io5";

function PrivateMessage({ currentUserId }) {
    const [conversations, setConversations] = useState([]);
    const [selectedConversationId, setSelectedConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
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

            setLoading(true);

            // Fetch messages for the selected conversation
            fetch(`http://localhost:8000/api/conversation/${selectedConversationId}/messages/`)
                .then(response => response.json())
                .then(data => {
                    setMessages(data.messages);
                    setLoading(false);
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
        <div className="container">
            <div className="conversations">
                <h2>Chats</h2>
                {conversations.map(conversation => (
                <div key={conversation.id} onClick={() => setSelectedConversationId(conversation.id)}
                    className={conversation.id === selectedConversationId ? 'selected' : ''}>
                    {conversation.name}
                </div>
                ))}
            </div>
            <div className="messages">
                {selectedConversationId ? (
                    <div className='message-container'>
                        <h2>
                            {selectedConversation ? selectedConversation.name : ''}
                        </h2>
                        {loading ? (
                            <div>Loading...</div>
                        ) : (
                        <div className='message-inner-container'>
                            <div className="message-list">
                                {messages.map(message => (
                                <div key={message.id} className={message.sender_id === currentUserId ? 'from' : 'to'}>
                                    <div className='message'>
                                        {message.content}
                                    </div>
                                </div>
                                ))}
                            </div>
                            
                            <div className="text-input">
                                <input type="text" value={input} onChange={e => setInput(e.target.value)}
                                    onKeyPress={e => {
                                        if (e.key === 'Enter') {
                                            sendMessage();
                                        }
                                    }}
                                />
                                <button onClick={sendMessage}><IoSend /></button>
                            </div>
                        </div>
                        )}
                    </div>
                ) : (
                    <div>Select a conversation</div>
                )}
            </div>
      </div>
    );
}

export default PrivateMessage;
